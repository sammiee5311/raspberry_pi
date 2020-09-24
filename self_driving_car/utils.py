import cv2
import numpy as np

def thresholding(img):
    img_hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_white = np.array([[90,23,136]])
    upper_white = np.array([120,109,219])
    mask_white = cv2.inRange(img_hsv,lower_white,upper_white)
    return mask_white

def warp_img(img, points,w,h,inverse=False):
    point1 = np.float32(points)
    point2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    if inverse:
        matrix = cv2.getPerspectiveTransform(point2, point1)
    else:
        matrix = cv2.getPerspectiveTransform(point1, point2)

    img_warp = cv2.warpPerspective(img, matrix, (w,h))
    return img_warp

def nothing(a):
    pass

def initialize_trackbars(intial_tracbarVals,wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intial_tracbarVals[0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intial_tracbarVals[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intial_tracbarVals[2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intial_tracbarVals[3], hT, nothing)

def val_trackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points

def draw_points(img, points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]),int(points[x][1])), 15, (0,0,255), cv2.FILLED)

    return img

def get_histogram(img,display=False, min_per=0.1,region=1):

    if region == 1:
        histo_values = np.sum(img, axis=0) # axis of height
    else:
        histo_values = np.sum(img[img.shape[0]//region:,:], axis=0)

    max_value = np.max(histo_values)
    min_value = min_per*max_value

    index_arr = np.where(histo_values >= min_value)
    base_point = int(np.average(index_arr))

    if display:
        img_hist = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(histo_values):
            cv2.line(img_hist, (x,img.shape[0]), (x,img.shape[0]-(intensity//255//region)), (255,0,255), 1) # img.shape[0] = height / see how many # of pixels in each are on or off / intensity is opposite direction so it needs to be subtracted by height
            cv2.circle(img_hist,(base_point,img.shape[0]),20,(0,255,255),cv2.FILLED)
        return base_point, img_hist

    return base_point


def stack_images(scale,img_array):
    rows = len(img_array)
    cols = len(img_array[0])
    rows_available = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]
    if rows_available:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if img_array[x][y].shape[:2] == img_array[0][0].shape [:2]:
                    img_array[x][y] = cv2.resize(img_array[x][y], (0, 0), None, scale, scale)
                else:
                    img_array[x][y] = cv2.resize(img_array[x][y], (img_array[0][0].shape[1], img_array[0][0].shape[0]), None, scale, scale)
                if len(img_array[x][y].shape) == 2: img_array[x][y]= cv2.cvtColor( img_array[x][y], cv2.COLOR_GRAY2BGR)
        image_blank = np.zeros((height, width, 3), np.uint8)
        hor = [image_blank]*rows
        hor_con = [image_blank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = cv2.resize(img_array[x], (0, 0), None, scale, scale)
            else:
                img_array[x] = cv2.resize(img_array[x], (img_array[0].shape[1], img_array[0].shape[0]), None,scale, scale)
            if len(img_array[x].shape) == 2: img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(img_array)
        ver = hor
    return ver