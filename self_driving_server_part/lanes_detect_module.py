import numpy as np
import time
from points_generate_module import points_generate_module


def lanes_detect_module(frame, Hough_lines):
    highway_lanes = []

    # 무빙 에버리징
    straight_line_num = 0
    if Hough_lines is None:
        return highway_lanes, straight_line_num

    height, width, depth = frame.shape
    left_candidates = []
    right_candidates = []

    # 중요한 코드
    half = 1/2
    left_area = width * half
    right_area = width * half

    for line in Hough_lines:
        for x0, y0, x1, y1 in line:
            if x0 == x1: # 직진 주행
                straight_line_num += 1 # 이 변수로 튀는 값을 잡아준다
                if straight_line_num >=3 : # 무빙 에버리징을 위한 조건문
                    straight_line_num = 2
                print("직진합니다!!!!!!!!")
                time.sleep(0.1) # dc모터 보정을 위하여

                continue
                
 
            slope = (y1 - y0) / (x1 - x0) # 기울기
            intercept = y0 - (x0 * slope) # y절편

            if slope < 0:  # 좌회전 
                if x0 < left_area and x1 < left_area:
                    left_candidates.append((slope, intercept))
            else:  # 우회전
                if x0 > right_area and x1 > right_area:
                    right_candidates.append((slope, intercept))

    left_average = np.average(left_candidates, axis=0)
    if len(left_candidates) > 0:
        highway_lanes.append(points_generate_module(frame, left_average))

    right_average = np.average(right_candidates, axis=0)
    if len(right_candidates) > 0:
        highway_lanes.append(points_generate_module(frame, right_average))

  
    return highway_lanes, straight_line_num