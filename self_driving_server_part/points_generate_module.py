def points_generate_module(frame, line):
    height, width, depth = frame.shape

    slope, intercept = line

    y0 = height
    y1 = int(height / 2)

    if slope == 0: # 기울기 보정
        slope = 0.1

    # x = (y - y절편) / 기울기 
    x0 = int((y0 - intercept) / slope) 
    x1 = int((y1 - intercept) / slope) 

    return [[x0, y0, x1, y1]]
