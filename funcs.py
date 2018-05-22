import cv2
import numpy as np
import math


def findHand(img):

    original = img

    h, w, pix = img.shape

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #return cv2.cvtColor(img,cv2.COLOR_GRAY2RGB), 0, 0

    img = cv2.GaussianBlur(img, (25, 25), 0)

    #return cv2.cvtColor(img,cv2.COLOR_GRAY2RGB), 0, 0

    _, thresh = cv2.threshold(img, 85, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_NONE)[-2:]

    img = cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB)
    #return img, 0, 0

    mask = np.zeros(img.shape, np.uint8)
    contour = 0

    max_area = -1

    for i in range(len(contours)):
        contourTest = contours[i]
        area = cv2.contourArea(contourTest)
        if (area > max_area):
            max_area = area
            contour = contours[i]

    img1 = img
    img = original

    highest = 0
    highestFinger = 0
    fingerCount = 0

    if type(contour) is not int:

        img = drawKeyboard(img)
        mask = np.zeros(img.shape, np.uint8)
        cv2.drawContours(mask, contour, -1, (0, 0, 255, 0), 1)
        img = cv2.add(mask, img)

        cv2.drawContours(mask, contour, -1, (0, 255, 255, 255), 5)
        img1 = cv2.add(mask, img1)
        #return img1, 0, 0

        hull = cv2.convexHull(contour)
        drawing = np.zeros(img.shape, np.uint8)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255, 255), 1)
        img1 = cv2.add(drawing, img1)
        #return img1, 0, 0

        hull = cv2.convexHull(contour, returnPoints=False)
        concav = cv2.convexityDefects(contour, hull)

        if concav is not None:
            _, highestFinger, _, _ = concav[0, 0]
            highestFinger = tuple(contour[highestFinger][0])
            for i in range(concav.shape[0]):
                start, end, far, dist = concav[i, 0]
                start = tuple(contour[start][0])
                end = tuple(contour[end][0])
                far = tuple(contour[far][0])
                a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                angle = math.acos((b**2 + c**2 - a**2) / (2 * b * c)) * 57
                if angle <= 90 and dist > 20:
                    if end[1] < highestFinger[1]:
                        highestFinger = end
                    fingerCount += 1
                    img = drawTip(img, end)
                    #img = drawDef(img,far)

            highestFinger = highestFinger[1]
            cv2.line(img, (0, highestFinger), (w, highestFinger), (0, 255, 0))
            highest = 1.0000000001 * highestFinger / h

    return img, highest, fingerCount


def vLine(img, percent):

    h, w, pix = img.shape

    k = 1.000001

    cv2.line(img, (int(k * percent * w), 0), (int(k * percent * w), h),
             (0, 255, 0))

    return img


def hLine(img, percent):

    h, w, pix = img.shape

    k = 1.000001

    cv2.line(img, (0, int(k * percent * h)), (w, int(k * percent * h)),
             (0, 255, 0))

    return img


def drawTip(img, position):

    cv2.circle(img, position, 12, [51, 0, 255], 2)
    cv2.circle(img, position, 5, [51, 153, 255], 1)
    cv2.circle(img, position, 3, [102, 255, 255], 1)

    return img


def drawDef(img, position):

    cv2.circle(img, position, 12, [51, 255, 0], 2)
    cv2.circle(img, position, 5, [51, 255, 102], 1)
    cv2.circle(img, position, 3, [255, 255, 100], 1)

    return img


def drawKeyboard(img):

    h, w, pix = img.shape
    mask = np.zeros(img.shape, np.uint8)

    for i in range(12):
        cv2.line(img, (0, int(i * h / 12)), (int(0.1 * w), int(i * h / 12)),
                 (0, 0, 0))
        cv2.line(img, (int(0.9 * w), int(i * h / 12)), (w, int(i * h / 12)),
                 (0, 0, 0))

    return cv2.add(mask, img)
