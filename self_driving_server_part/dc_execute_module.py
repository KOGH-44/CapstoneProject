import RPi.GPIO as GPIO  # 라즈베리파이 GPIO 활용을 위하여
import time


def dc_execute_module():
    GPIO.setmode(GPIO.BCM)  # BOARD 모드와 BCM 모드 중 BCM 모드로 세팅
    dc_pin = 23  # 23번을 활용하여 DC모터 컨트롤

    # 23번을 출력 단자로 설정 (DC 모터 & L298N 모터 드라이버 연동)
    GPIO.setup(dc_pin, GPIO.OUT, initial=GPIO.LOW)

    dc_motor = GPIO.PWM(dc_pin, 100)  # PWM 100Hz의 주파수 설정
    dc_motor.start(40)  # 듀티 사이클 40% 세팅
    time.sleep(0.13)  # 0.13초 슬립 (토크가 완전히 걸리기 위하여 어쩔수 없는 선택)
    dc_motor.stop()

