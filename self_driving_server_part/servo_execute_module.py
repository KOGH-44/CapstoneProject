import RPi.GPIO as GPIO
import time


def servo_execute_module(input_angle):
     GPIO.setmode(GPIO.BCM)  # BOARD 모드와 BCM 모드 중 BCM 모드로 세팅
     servo_pin = 18 # 18번을 활용하여 서보모터 컨트롤
     GPIO.setup(servo_pin, GPIO.OUT)  # 23번을 출력 단자로 설정
     servo = GPIO.PWM(servo_pin, 50)
    
     if input_angle > 87: # 자동차 구조상 최대 좌회전값 (좌회전)
         input_angle = 87
     elif input_angle < 14: #자동차 구조상 최대 우회전값 (우회전)
         input_angle = 14 
     duty = input_angle / 180 * 12.5 # 입력 각도 값을 듀티값으로 변환하는 식
    
     servo.start(duty) # 회전각에 따라 회전
     time.sleep(0.02) # 0.02초간 딜레이를 걸어줌
     servo.stop() 
     GPIO.cleanup() 

  
    
    
    
    
    
    
    
    
    
    
    
    
    #servo_min_duty = 3 # 최소 듀티비 (서보모터 0도로 이동시키게 됨) 3.05 => 1도 3.10 => 2도 (실험을 통해 바꾸면서 설정하기 (꼭 3이 아닐수도 있음))
    #servo_max_duty = 12.5 # 최대 듀티비 (서보모터 180도로 이동시키게 됨) 11.95 => 179도 (실험을 통해 바꾸면서 설정하기 (꼭 12가 아닐수도 있음))


    #def set_servo_angle(angle):    # 각도를 입력하면 듀티비를 알아서 설정해주는 함수
        # 각도는 최소0, 최대 180으로 설정
        #if angle > 180:
            #angle = 180
        #elif angle < 0:
            #angle = 0

        # 입력한 각도(angle)를 듀티비로 환산하는 식
        #duty = servo_min_duty+(angle*(servo_max_duty-servo_min_duty)/180.0)
        #duty = (angle/180*12.5)
        # 환산한 듀티비를 서보모터에 전달
        #servo.ChangeDutyCycle(duty)
    
    #for i in range(0,80, 3):
        #set_servo_angle(i)
        #time.sleep(0.1)
        #print(i)
  

#for ii in range (5,80, 3):
    #servo_execute(ii)
#servo_execute(25) # 우회전
#servo_execute(41) # 좌회전
    