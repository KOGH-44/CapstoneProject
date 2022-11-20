import numpy as np
import cv2


def ROI_module(edges):
    height, width = edges.shape
    mask = np.zeros_like(edges)

    roi_area = np.array([[
        (0, height),
        (0, height/2),
        (width, height/2),
        (width, height),
    ]], np.int32)

    cv2.fillPoly(mask, roi_area, 255)

    roi = cv2.bitwise_and(edges, mask)

    return roi
