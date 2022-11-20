import cv2  # opencv 라이브러리 추가
import dlib  # dlib 라이브러리 추가
from scipy.spatial import distance # 원소 간 유클리드 거리 계산 용도
from playsound import playsound  # 알람 발생 용도
import winsound  # 알람 발생 용도
import socket  # 소켓 통신용 라이브러리 추가


#HOST = '127.0.0.1' # localhost
HOST = '192.168.137.160'  # 소켓 통신을 위한 IP 주소 (본인 IP 상황에 맞게 변경 요함)
PORT = 9999  # 포트 번호

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 소켓 인스턴스 생성 ################################
client_socket.connect((HOST, PORT))  # 소켓 연결 ################################


def calculate_EAR(eye_coordinates):  # EAR (Eye Aspect Ratio (눈 종횡비)) 계산 함수 정의
    # 유클리드 거리 계산
    height_of_eye_0 = distance.euclidean(eye_coordinates[1], eye_coordinates[5])
    height_of_eye_1 = distance.euclidean(eye_coordinates[2], eye_coordinates[4])
    width_of_eye = distance.euclidean(eye_coordinates[0], eye_coordinates[3])

    Eye_Aspect_Ratio = (height_of_eye_0 + height_of_eye_1) / (2.0 * width_of_eye)

    return Eye_Aspect_Ratio


# 카메라 객체 생성
#cap = cv2.VideoCapture("driving_woman_sample.mp4") # 운전중인 외국인 여성 영상 (샘플)
#cap = cv2.VideoCapture("drowsiness_detection_video_me.mp4") # 본인의 졸음 운전 영상
cap = cv2.VideoCapture(0) # 카메라로 실시간 캡쳐 (운전자의 얼굴을 촬영)

hog_face_detector = dlib.get_frontal_face_detector() # Histogram of Oriented Gradients
dlib_facelandmark = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # dlib 라이브러리가 데이터 세트를 사용하여 얼굴 감지 객체 생성
#dlib_facelandmark = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat") 


# 전역 변수 및 플래그 값 초기화 작업
drowsiness_frame = 0  # 졸음 프레임 초기화
all_frame = 0  # 전체 프레임 초기화
status_flag = False  # 상태 플래그 초기화
send_message = True  # 소켓 통신 플래그 초기화
quit_flag = False  # 종료 플래그 초기화


while True:  # 졸음 감시 반복
    print(all_frame)  
    print(drowsiness_frame)  
    _, frame = cap.read()  # 카메라로 읽어들이기
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 컬러 스페이스를 그레이 스케일로 변환 (속도 최적화 위한 변환)
    
    face_detection = hog_face_detector(gray_frame) # shape_predictor_68_face_landmarks.dat 에 기반
    
    for face in face_detection: # 좌표값에 관한 반복문 실행
        face_landmarks = dlib_facelandmark(gray_frame, face)
        left_eye = []
        right_eye = []

        '''눈 좌표 저장 및 눈 그리기 '''
        for nth in range(36, 42):  # 왼쪽 눈 계산
            x_curr = face_landmarks.part(nth).x
            y_curr = face_landmarks.part(nth).y
            left_eye.append((x_curr, y_curr))
            next_point = nth + 1
            if nth == 41: # 끝일 경우
                next_point = 36 # 리프레쉬
            # 업데이트
            x_next = face_landmarks.part(next_point).x
            y_next = face_landmarks.part(next_point).y
            
            cv2.line(frame, (x_curr, y_curr), (x_next, y_next), (255, 255, 0), 1)

        for nth in range(42, 48):  # 오른쪽 눈 계산
            x_curr = face_landmarks.part(nth).x
            y_curr = face_landmarks.part(nth).y
            right_eye.append((x_curr, y_curr))
            next_point = nth + 1
            if nth == 47: # 끝일 경우
                next_point = 42 # 리프레쉬
            # 업데이트
            x_next = face_landmarks.part(next_point).x
            y_next = face_landmarks.part(next_point).y

            cv2.line(frame, (x_curr, y_curr), (x_next, y_next), (255, 255, 0), 1)


        # EAR 계산
        left_ear = calculate_EAR(left_eye)
        right_ear = calculate_EAR(right_eye)

        EAR = (left_ear + right_ear) / 2  # 왼쪽 눈과 오른쪽 눈의 EAR의 평균값 계산
        EAR = round(EAR, 2)
        #EAR = round(EAR, 2)  # 소수점 2째자리까지 반올림
        if EAR <= 0.15 and status_flag is not True:  # Eye Aspect Ratio 공식에 따라 나온 값이 0.05 이하일 경우 (0.05부터 닫힌눈이라 판단, 출처: Drowsiness Detection Based on Facial Landmark and Uniform Local Binary Pattern (Journal of Physics: Conference Series)) # 사람에 따라 변경이 필요
            # https://iopscience.iop.org/article/10.1088/1742-6596/1529/5/052015/pdf
            cv2.putText(frame, "WARNING!", (150, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (1, 1, 255), 3, cv2.LINE_8)  # 졸음 운전 경고 문구 출력
            if all_frame > 15:  # 초기값 버려주는 행위로 인한 보정
                drowsiness_frame += 1 # 졸음 프레임 값 1 증가
        all_frame += 1  # 전체 프레임 값 1 증가
    

    if status_flag is True: 
        cv2.putText(frame, "SELF-DRIVING MODE", (100, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (155, 250, 1), 1, cv2.LINE_8)  # 자율 운전 모드로 변환하였다는 메시지 출력
        client_socket.send('S'.encode()) ################################
        
    else:    
        pass
        client_socket.send('R'.encode()) ####################################

    if quit_flag is True:
        client_socket.send('Q'.encode()) ###################################
        pass
        
        

    cv2.imshow("Drowsiness Detection (Client)", frame)  # 이미지 출력
    
    if(all_frame > 15):  # 초반 프레임 보정
        if ((drowsiness_frame / all_frame) >= 0.15):  # (졸음 시간 / 전체 시간) (PERCLOS) 비율 판단 (PERCLOS 0.15 이상이면 졸음 상태라 정의함, 출처: 눈깜박임과 심박수를 이용한 졸음 경고 시스템 (한국컴퓨터정보학회 하계학술대회 논문집 제29권 제2호 (2021. 7)))
            # http://www.koreascience.or.kr/article/CFKO202125036570394.pdf
            if status_flag is not True:
                winsound.PlaySound("warning_alarm_sound.wav", winsound.SND_ASYNC | winsound.SND_LOOP)  # 졸음을 깨기 위한 알람을 비동기로 발생
                status_flag = True  # 상태 플래그 변경 (자율 주행 모드 실행을 위하여)
                print("WARNING!!!!!!!!!!!!!!") 


    key = cv2.waitKey(16) # 60 FPS

    if key == ord('r'):  # 알람을 해제하고 모든 변수 초기화 및 수동 운전 모드로 전환 (자율 주행 해제)
        status_flag = False
        drowsiness_frame = 0
        all_frame = 0
        winsound.PlaySound(None, winsound.SND_ASYNC)  # 졸음을 깨기 위한 알람을 비동기로 종료
    
    elif key == ord('s'):  # (실험용) 자율 주행 시작
        status_flag = True
        
    elif key == ord('q'):  # 프로그램 종료키 입력
        quit_flag = True
        #break
       
        
cap.release()  # 메모리 해제
cv2.destroyAllWindows()  # 프로그램 종료

