# !/usr/bin/python37
# Raspberry pi 3/3B+/4B, OpenCV 4.2.0, Thonny 3.7.3
# Date: 4h March, 2020

import cv2
import numpy as np
import math
from scipy import stats
def linregress(points):
    x=[]
    y=[]
    for point in points:
        x.append(point[0])
        y.append(point[1])
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    p1=[max(x),slope*max(x)+intercept]
    p2=[min(x),slope*min(x)+intercept]
    return p1,p2
print(linregress([[0,0],[1,1]]))

def angle_with_x_axis(point1, point2):
    if point1[0] == point2[0]:
        # Handle the case where the line is vertical
        return 0.0

    # Calculate the rise and run
    rise = point2[1] - point1[1]
    run = point2[0] - point1[0]

    # Calculate the angle using atan2 (in radians)
    angle_radians = math.atan2(rise, run)

    # Convert radians to degrees
    angle_degrees = math.degrees(angle_radians)

    # Ensure the angle is between 0 and 360 degrees
    angle_degrees = (angle_degrees + 360) % 360

    return angle_degrees


# def coordinates(contour):
#     #given many points in the space, we make a approximate shape and find the min and max X and Y values of the shape
#     approx = cv2.approxPolyDP(contour, 0.009 * cv2.arcLength(contour, True), True)
#     n = approx.ravel()
#     i = 0
#     maxX = maxY = minX = minY = 0
#     for j in n:
#         if (i % 2 == 0):
#             # if(minX is -1):
#             #     minX = n[i]
#             # if (minY is -1):
#             #     minY = n[i + 1]
#             if(n[i] < n[minX]):
#                 minX = i
#             if (n[i] > n[maxX]):
#                 maxX = i
#             if(n[i+1] < n[minY]):
#                 minY = i+1
#             if (n[i+1] > n[maxY]):
#                 maxY = i+1
#         i=i+1
#     return n[maxX],n[maxX+1],n[maxY-1],n[maxY],n[minX],n[minX+1],n[minY-1],n[minY]
def find_line(points):
    arr = []
    best_arr = []
    for z in points:
        for z2 in points:
            arr = [z, z2]
            if not z is z2:
                line_angel = angle_with_x_axis(z, z2)
                for z3 in points:
                    if z3 is not z2 and z3 is not z:
                        if abs(angle_with_x_axis(z2, z3) - line_angel) < 10:
                            arr.append(z3)
                if len(arr) > len(best_arr):
                    best_arr = arr
                arr = []
    return best_arr
def find_contours(img_name, threshold, thr_reset):
    img = cv2.imread(img_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray,
                               (15, 15), 6)
    # all pixels value above value_1 will
    # be set to value_2
    ret, thresh = cv2.threshold(blurred,
                                threshold, thr_reset,
                                cv2.THRESH_BINARY)

    contours, hier = cv2.findContours(thresh.copy(),
                                      cv2.RETR_TREE,
                                      cv2.CHAIN_APPROX_SIMPLE)
    lpoints = []
    rpoints=[]
    for c in contours:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 500 or cv2.contourArea(c) > 20000:
            continue

        # get the min area rect
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        # convert all coordinates floating point values to int
        box = np.int0(box)
        print(box)
        # draw a red 'nghien' rectangle
        cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
        # cv2.imwrite('zebra_lane1.jpg', img)
        # cv2.imshow("contours", img)
        x, y, w, h = cv2.boundingRect(c)
        lpoints.append((x, y))
        rpoint.append((x+w,y))


    length = len(points)
    if length < 3:
        return None
    print('len=', length)
    best_left=find_line(lpoints)
    best_right=find_line(rpoints)

    for point in best_left:
        print(point)
        cv2.circle(img, point, radius=5, color=(0, 0, 255), thickness=-1)
    for point in best_right:
        print(point)
        cv2.circle(img, point, radius=5, color=(0, 0, 255), thickness=-1)
    z=best_arr[0]
    z2=best_arr[1]
    cv2.line(img, (z2[0], z2[1]), (z[0], z[1]), (0, 0, 0), 9)
    cv2.imshow("contours", img)
    key = cv2.waitKey(5000)
    print("console.log()")
    return img

first="img1.jpeg"
second='zebra.jpg'
# cv2.imshow("contours", img)
# find_contours("zebra.jpg",180,255)
for i in range(120,190,10):
    for j in range(80,100,10):
        print("params: ",i,j)
        my_img = find_contours(second, i, j)
        if my_img is None:
            continue
        cv2.imshow("contours", my_img)
        key = cv2.waitKey(500)




cv2.destroyAllWindows()
