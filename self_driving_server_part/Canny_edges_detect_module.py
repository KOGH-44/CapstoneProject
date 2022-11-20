import cv2
import numpy as np


def Canny_edges_detect_module(original_input_frame):

    gray_frame = cv2.cvtColor(original_input_frame, cv2.COLOR_BGR2GRAY) # 그레이 스케일 변환 (속도 관련)
    #tvalue_otsu, t_otsu = cv2.threshold(gray_frame, -1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 
    #print(tvalue_otsu)
    adaptive_Gaussian_frame = cv2.adaptiveThreshold(gray_frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
        cv2.THRESH_BINARY, 9, 5) # 적응형 쓰레시홀딩을 통해 조명에 따른 오차를 줄일수 있다. (지역적으로 나누어 판단하므로)
    
    #mask = cv2.inRange(t_otsu, 0, 50) 
    mask = cv2.inRange(adaptive_Gaussian_frame, 0, 50) # 마스킹 작업 수행

    # 엣지 검출 
    #cv2.imshow("otsu", t_otsu)
    #cv2.imshow("adaptive_Gaussian", adaptive_Gaussian_frame)
    edges = cv2.Canny(mask, 55, 110)
    # cv2.imshow("edges",edges)

    return edges
