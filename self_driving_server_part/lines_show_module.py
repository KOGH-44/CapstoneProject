import cv2
import numpy as np


def lines_show_module(frame, lines, line_color=(175, 200, 50), line_width=6):
    line_parts = np.zeros_like(frame)

    if lines is not None:
        for line in lines:
            for x0, y0, x1, y1 in line:
                cv2.line(line_parts, (x0, y0), (x1, y1),
                         line_color, line_width)

    line_parts = cv2.addWeighted(frame, 0.9, line_parts, 1, 1)

    return line_parts
