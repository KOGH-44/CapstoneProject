import cv2
import numpy as np


def Hough_lines_detect_module(roi):
    Hough_lines = cv2.HoughLinesP(roi, 1, np.pi/180,
                           10, np.array([]), minLineLength=5, maxLineGap=150)

    #Hough_lines = cv2.HoughLines(roi, 1, np.pi/180, 10) # μλ λΉκ΅

    return Hough_lines
