import socket # 소켓 통신용
import cv2 # 이미지 처리용
import numpy as np 
import math 
import time # 수행 시간 비교측정용
import threading # 멀티스레드용

''' 개인 정의 모듈 '''
from lanes_detect_module import lanes_detect_module
from Canny_edges_detect_module import Canny_edges_detect_module
from steering_angle_calculate_module import steering_angle_calculate_module
from Hough_lines_detect_module import Hough_lines_detect_module
from ROI_module import ROI_module
from direction_vectors_display_module import direction_vectors_display_module
from lines_show_module import lines_show_module
from servo_execute_module import servo_execute_module
from dc_execute_module import dc_execute_module


#HOST = '127.0.0.1' # Localhost
HOST = '192.168.137.160' # 소켓 통신 IP 주소 (본인에 맞게 변경 요함)
PORT = 9999 # 포트 

# 서버 소켓 세팅 (socket, bind, listen)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

# 종료용 플래그 변수
finish_count = 0

while True: 
    print('대기중')
    client_socket, addr = server_socket.accept() # 서버-클라이언트 통신 수락까지 대기후 아래 코드 수행
    print('[Client-Server] Connection Complete') 
    
    # 맨 처음 시작할때 서보모터 정면각을 맞춰주기 위한 플래그
    once_start_flag = True

    # 모듈을 끝낼 때 사용할 플래그
    finish_module_flag = False

    # DC 모터 구동을 위한 플래그
    DC_flag = False
    
    while True: # 한번의 시퀀스가 일어날때 (모니터를 켜서 얼굴을 감시할 때 이 반복문을 계속 반복한다.) (S or R 시퀀스)      
                                    
            data = client_socket.recv(10) # data 에는 문자 s(self-driving mode), 문자 r(release), 문자 q(quit program) 중 하나가 올 수 있다. 
            if data.decode('utf-8') is 'Q': 
                finish_module_flag = True
                break
            
            video = cv2.VideoCapture(0) # 자동차에 달린 웹캠으로 도로의 이미지를 받아드린다
            video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            x_vec_array = [] # 무빙 에버리징을 위한 0으로 가득찬 배열 생성 (3개의 평균값을 이용하여 방향 결정 (노이즈 최소화))
            
            # 초기 각도 세팅
            global global_steering_angle
            global_steering_angle = 33 #  global_steering_angle 변수는 차체의 구조적 이유때문에 0에서123까지의 값을 가질수 있다.
            
            if once_start_flag is True: # 맨 처음 초기 세팅
                servo_execute_module(33) # 33도는 자동차 기준 정면입니다.
                once_start_flag = False
            
            DC_count = 0 # 안쪽 while문에서 사용할 카운트 변수
            if data.decode('utf-8') is 'S': # 이 시점에 문자 'S'를 받으면 DC_flag를 참으로 바꾸고 DC 모터를 한번 켜주고 다음 while문을 실행
                DC_flag = True
            
            # 맨 처음 방향 초기화용 변수
            motor_exe_cnt = 0
            if DC_flag is True:
                motor_exe_cnt += 1
            
            
            while True: # 문자 s 혹은 문자 r이 들어왔을 경우 돌아가는 반복문
                
                if finish_module_flag is True:
                    break

                data = client_socket.recv(10) # 소켓 통신으로 문자 받기
                
        
                if data.decode('utf-8') is 'Q': # 이 시점에 문자 'Q'를 받으면 finish_module_flag를 참으로 바뀌고 프로그램 종료
                    finish_module_flag = True
                    client_socket.close()    
                    server_socket.close()
                    break
                
                if data.decode('utf-8') is 'S': 
                    #TIME_1 = time.time() # 셀프 드라이빙 한 시작점의 시각 
                    # 멀티스레드 처리 (DC모터 (토크값으로 인하여))
                    t = threading.Thread(target=dc_execute_module) # Thread create (코드 속도 최적화를 위하여)
                    t.start() # 멀티스레드 시작 코드 (DC모터 스레드로 따로 구동)
                    
                    DC_flag = True
                    
                    if DC_flag is True and DC_count == 0 and motor_exe_cnt == 0:
                        
                        DC_count += 1
                        

                    ret, frame = video.read()

                    ''' 자율주행 알고리즘 '''
                    edges = Canny_edges_detect_module(frame)
                    roi = ROI_module(edges)
                    Hough_lines = Hough_lines_detect_module(roi)
                    highway_lanes, straight_line_num = lanes_detect_module(frame, Hough_lines)
                    highway_lanes_parts = lines_show_module(frame, highway_lanes)
                    steering_angle = steering_angle_calculate_module(frame, highway_lanes)
                    #print(f'angle: {steering_angle}도')

                    result_frame, x_vec = direction_vectors_display_module(highway_lanes_parts, steering_angle)
                    
                    ''' 직진으로 인한 에버리징 보정을 위한 처리 (조건에 따라 인큐잉, 디큐잉 반복) '''
                    if straight_line_num is 0:
                        pass
                    elif straight_line_num is 1:
                        x_vec_array.append(0)
                        if len(x_vec_array) is 3:
                            x_vec_array.pop(0)
                        elif len(x_vec_array) is 4:
                            x_vec_array.pop(0)
                            x_vec_array.pop(0)
                    elif straight_line_num is 2:
                        x_vec_array.append(0)
                        x_vec_array.append(0)
                        if len(x_vec_array) is 3:
                            x_vec_array.pop(0)
                        elif len(x_vec_array) is 4:
                            x_vec_array.pop(0)
                            x_vec_array.pop(0)
                        elif len(x_vec_array) is 5:
                            x_vec_array.pop(0)
                            x_vec_array.pop(0)
                            x_vec_array.pop(0)
        
                    
                    ''' 무빙 에버리징 알고리즘 '''
                    x_vec_array.append(x_vec) # 프레임 마다 나오는 x_vec(방향을 위한)값을 배열에 추가
                    if len(x_vec_array) is 3 :
                        moving_averaging_list_sum = sum(x_vec_array)
                        moving_average = moving_averaging_list_sum / 3 # ??? angle? x_vec?
        
                        real_angle_tan = moving_average / 240 # 240은 y축의 길이
                        real_angle = math.degrees(math.atan(real_angle_tan)) # 실제 각 구하기
                        #print(f'real angle: {real_angle}') # 우리가 이 값을 활용하여 서보모터를 제어함
                        x_vec_array.pop(0) # 젤 처음값 제거

                        # global_steering_angle 변수를 가지고 식을 방정식을 만들어서 그 값을 servo모터를 움직여줘야함
                        #global_steering_angle = global_steering_angle + (90 - real_angle ) # 전역 각도 제어 변수에 추가해줄값을 더하여 전역 각도 제어 값 리프레시
                        global_steering_angle = global_steering_angle - real_angle
                        if global_steering_angle > 88: # 자동차 구조상 최대값 처리 
                            global_steering_angle = 88
                        elif global_steering_angle < 13: # 자동차 구조상 최소값 처리
                            global_steering_angle = 13
                        
                        servo_execute_module(global_steering_angle) # 서보 모터 구동 (회전각 만큼 회전)
                    
                    # 통합하여 보는 경우    
                    #cv2.imshow("Result image", result_frame)
                    # coupled = np.vstack((frame, result_frame))
                    # cv2.imshow("Total", coupled)
                    
                    cv2.moveWindow("Result image (Server)", 0, 0) # 윈도우창 시작 위치 보기 좋게 조정 
                    cv2.imshow("Result image (Server)", result_frame) # 결과 화면 출력
                    
                    key = cv2.waitKey(16) # 60fps
                    t.join() # 멀티스레드 종료 코드
                    #TIME_2 = time.time() # 셀프 드라이빙 한 종료점의 시각
                    #time_all = TIME_2 - TIME_1 # 멀티 스레드로 인한 최적화 시간 측정
                    #print(time_all)
                    if key == 27: # ESC 누를 경우 브레이크
                        break
                
                elif data.decode('utf-8') is 'R': # Release 값을 클라이언트로 입력받고 수동 운전 상태로 돌아가게 하는 부분
                    video.release()
                    cv2.destroyAllWindows()
                    if DC_flag is True:
                        DC_flag = False
                    break

                
            #video.release()
            # out.release()
            # out2.release()
            #cv2.destroyAllWindows()

            if finish_module_flag is True: # 서버-클라이언트간 통신 종료 코드
                finish_count += 1
                print('[Client-Server] Connection Destroy')
                break
                      
             
    client_socket.close()
    break 

if finish_module_flag is True and finish_count is 0: # 서버-클라이언트간 통신 종료
    print('[Client-Server] Connection Destroy')

# 서버-클라이언트 연결 종료
client_socket.close()    
server_socket.close()