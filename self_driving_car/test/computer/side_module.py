import cv2
import numpy as np


class Object_Location:
    def get_alternative_steering_value(self, img, x, w):
        height, width, _ = img.shape
        middle_point = width // 2
        far_percentage, direction = 1, None
        if middle_point < x:
            far_percentage = float((x - middle_point) / middle_point) * 100
            direction = 'LEFT'
        elif x < middle_point < x + w:
            right_percentage, left_percentage = float((middle_point - x) / middle_point), float((x + w - middle_point) / middle_point)
            if left_percentage > right_percentage:
                far_percentage = 100 - left_percentage * 100
                direction = 'LEFT'
            else:
                far_percentage = 100 - right_percentage * 100
                direction = 'RIGHT'
        elif x + w < middle_point:
            far_percentage = float(((x + w - middle_point) / middle_point)) * 100
            direction = 'RIGHT'

        return far_percentage, direction






