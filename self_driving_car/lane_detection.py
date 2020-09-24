import cv2
import numpy as np
import utils
from collections import deque

curve_deque = deque()
curve_list = []
avg_val = 10


def get_lane_curve(img, display=2): # 0 = not display / 1 = display the result only / 2 = display everything

    # intial_trackbar_values = [125,88,24,226]
    # utils.initialize_trackbars(intial_trackbar_values)
    img_original = img.copy()
    img_result = img.copy()
    #### STEP 1
    img_thres = utils.thresholding(img)

    #### STEP 2
    hT, wT, c = img.shape
    points = utils.val_trackbars()
    img_warp = utils.warp_img(img_thres,points,wT,hT)
    img_wrap_points = utils.draw_points(img_original, points)

    #### STEP 3
    mid_point, img_hist = utils.get_histogram(img_warp, display=True, min_per=0.5, region=4)
    curve_avg_point, img_hist = utils.get_histogram(img_warp, display=True, min_per=0.9)
    curve_raw = curve_avg_point-mid_point

    #### STEP 4
    curve_deque.append(curve_raw)
    if len(curve_deque) > avg_val:
        curve_deque.popleft()

    curve = int(sum(curve_deque)/len(curve_deque))

    #### STEP 5
    if display != 0:
        img_inv_warp = utils.warp_img(img_warp, points, wT, hT, inverse=True)
        img_inv_warp = cv2.cvtColor(img_inv_warp, cv2.COLOR_GRAY2BGR)
        img_inv_warp[0:hT // 3, 0:wT] = 0, 0, 0
        img_lane_color = np.zeros_like(img)
        img_lane_color[:] = 0, 255, 0
        img_lane_color = cv2.bitwise_and(img_inv_warp, img_lane_color)
        img_result = cv2.addWeighted(img_result, 1, img_lane_color, 1, 0)
        midY = 450
        cv2.putText(img_result, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(img_result, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(img_result, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(img_result, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        # cv2.putText(img_result, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        img_stacked = utils.stack_images(0.7, ([img, img_wrap_points, img_warp],
                                             [img_hist, img_lane_color, img_result]))
        cv2.imshow('ImageStack', img_stacked)

    elif display == 1:
        cv2.imshow('Resutlt', img_result)

    ####  NORMALIZATION

    curve = curve/100
    if curve > 1:
        curve = 1
    elif curve < -1:
        curve = -1

    cv2.imshow('Thres', img_thres)
    cv2.imshow('Wrap', img_warp)
    cv2.imshow('Wrap points', img_wrap_points)
    cv2.imshow('img_hist', img_hist)

    return curve


if __name__ == '__main__':
    cap = cv2.VideoCapture('test.mp4')
    intial_trackbar_values = [125,88,24,226]
    utils.initialize_trackbars(intial_trackbar_values)
    frameCounter = 0
    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        success, img = cap.read()
        # img = cv2.imread('1234.jpg')
        img = cv2.resize(img,(480,240))
        curve = get_lane_curve(img,display=2)
        print(curve)
        #cv2.imshow('img',img)
        cv2.waitKey(1)


