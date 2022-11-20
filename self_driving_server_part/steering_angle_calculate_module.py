import math # 아크탄젠트 함수를 활용하여 방향벡터 성분으로부터 회전각을 구해야함


def steering_angle_calculate_module(frame, highway_lanes):
    height, width, depth = frame.shape # 프레임 성분값 분해

    if len(highway_lanes) == 2: # 2개의 차선이 잡혔을 경우
        _, _, left_x2, _ = highway_lanes[0][0] # 성분 분해하여 좌측 x값 추출
        _, _, right_x2, _ = highway_lanes[1][0] # 성분 분해하여 우측 x값 추출
        mid_value = int(width / 2) # 중간값 계산
        x_ofs = (left_x2 + right_x2) / 2 - mid_value # 벡터 계산
        y_ofs = int(height / 2) # 벡터 계산

    elif len(highway_lanes) == 1: # 1개의 차선이 잡혔을 경우 (카메라각도에 의해)
        x0, _, x1, _ = highway_lanes[0][0] # 성분 분해하여 x값 2개 추출
        x_ofs = x1 - x0
        y_ofs = int(height / 2)

    else: # 그외
        x_ofs = 0
        y_ofs = int(height / 2)

    steering_angle_r = math.atan(x_ofs / y_ofs) # 분해된 벡터를 아크탄젠트를 활용하여 회전해야할 라디안각을 구함
    steering_angle_deg = int(steering_angle_r * 180.0 / math.pi) # 라디안각을 degree 각으로 변환

    steering_angle = steering_angle_deg + 90 # 90도 추가하여 변환 (시스템 구조상 필요)

    return steering_angle 
