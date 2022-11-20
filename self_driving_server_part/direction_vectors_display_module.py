import numpy as np
import cv2
import math


def direction_vectors_display_module(frame, steering_angle, line_color=(0, 0, 255), line_width=7):
    steering = np.zeros_like(frame)
    height, width, _ = frame.shape

    radian_angle = steering_angle / 180.0 * math.pi # 하나의 시점에 바퀴를 회전해야하는 각도

    x0, y0 = int(width / 2), height
    x1, y1 = int(x0 - height / 2 /math.tan(radian_angle)), int(height / 2) # x1 는 direction을 x축에 projection, y1 는 direction을 y축에 projection

    cv2.line(steering, (x0, y0), (x1, y1), line_color, line_width)
    
    cv2.line(steering, (x0, height-3), (x1, height-3), (0,255,200), 4) # x축 성분
    cv2.line(steering, (x0, y0), (x0, y1), (0,255,200), 4) # y축 성분
   
    x_vector = x1 - x0
    y_vector = y0 - y1
    #print("(%d, %d) " %(x_vector, y_vector)) # 분해된 벡터쌍 출력
    
    steering = cv2.addWeighted(frame, 0.9, steering, 1, 1) # 덫붙임

    return steering, x_vector
