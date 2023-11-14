# !/usr/bin/python37
# Raspberry pi 3/3B+/4B, OpenCV 4.2.0, Thonny 3.7.3
# Date: 4h March, 2020

import cv2
import numpy as np
import math
from scipy import stats


def is_getting_small(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]

    # Extract coordinates for Line 2
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    len1 = math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2)
    len2 = math.sqrt((x4 - x2) ** 2 + (y4 - y2) ** 2)


def angle_sum_vectors(angle1, angle2):
    # Convert angles to radians
    angle1_rad = math.radians(angle1)
    angle2_rad = math.radians(angle2)

    # Calculate the components of the vectors
    vector1_x = math.cos(angle1_rad)
    vector1_y = math.sin(angle1_rad)

    vector2_x = math.cos(angle2_rad)
    vector2_y = math.sin(angle2_rad)

    # Calculate the sum of the vectors
    sum_vector_x = vector1_x + vector2_x
    sum_vector_y = vector1_y + vector2_y

    # Calculate the magnitude of the sum vector
    magnitude_sum = math.sqrt(sum_vector_x ** 2 + sum_vector_y ** 2)

    # Calculate the angle between the sum vector and the x-axis
    angle_sum_rad = math.atan2(sum_vector_y, sum_vector_x)
    angle_sum_deg = math.degrees(angle_sum_rad)
    angle_sum_deg = (angle_sum_deg + 360) % 360
    return angle_sum_deg


def good_path(left_line, right_line):
    angle1 = angle_with_x_axis(left_line[0], left_line[1])
    angle2 = angle_with_x_axis(right_line[0], right_line[1])
    assert 0 < angle1, angle2 < 180
    print(angle1, angle2)
    direction = angle_sum_vectors(angle1, angle2)
    print(direction)
    good_zone_size = 20
    target = 270
    if target - good_zone_size < direction < target + good_zone_size:
        return 0
    if target - good_zone_size > direction:
        return -1
    else:
        return 1


def is_zebra(line1, line2):
    # Extract coordinates for Line 1
    x1, y1 = line1[0]
    x2, y2 = line1[1]

    # Extract coordinates for Line 2
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    # Calculate slopes and y-intercepts
    m1 = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')  # Avoid division by zero
    b1 = y1 - m1 * x1 if m1 != float('inf') else None

    m2 = (y4 - y3) / (x4 - x3) if (x4 - x3) != 0 else float('inf')  # Avoid division by zero
    b2 = y3 - m2 * x3 if m2 != float('inf') else None
    if m1 == m2:
        return False
    else:
        # Calculate the x-coordinate of the intersection point
        x_intersect = (b2 - b1) / (m1 - m2)
        y_intersect = x_intersect * m1 + b1
        # Check if the intersection point lies within the range of the line segments
        if y_intersect < min(y2, y4):
            return True
        else:
            return False


def is_intersect(line1, line2):
    # Extract coordinates for Line 1
    x1, y1 = line1[0]
    x2, y2 = line1[1]

    # Extract coordinates for Line 2
    x3, y3 = line2[0]
    x4, y4 = line2[1]

    # Calculate slopes and y-intercepts
    m1 = (y2 - y1) / (x2 - x1) if (x2 - x1) != 0 else float('inf')  # Avoid division by zero
    b1 = y1 - m1 * x1 if m1 != float('inf') else None

    m2 = (y4 - y3) / (x4 - x3) if (x4 - x3) != 0 else float('inf')  # Avoid division by zero
    b2 = y3 - m2 * x3 if m2 != float('inf') else None

    # Check if slopes are equal (parallel lines)
    if m1 == m2:
        return False
    else:
        # Calculate the x-coordinate of the intersection point
        x_intersect = (b2 - b1) / (m1 - m2)

        # Check if the intersection point lies within the range of the line segments
        if (x_intersect >= min(x1, x2) and x_intersect <= max(x1, x2)) and \
                (x_intersect >= min(x3, x4) and x_intersect <= max(x3, x4)):
            return True
        else:
            return False


def linregress(points):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    p1 = (max(x), int(slope * max(x) + intercept))
    p2 = (min(x), int(slope * min(x) + intercept))
    if p1[1] < p2[1]:
        return p2, p1
    return p1, p2


def angle_with_x_axis(point1, point2):
    if point1[0] == point2[0]:
        # Handle the case where the line is vertical
        return 90

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
    if len(points) < 3:
        return None
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


def check_lines(best_left, best_right, lpoints, rpoints):
    counter = 0
    for i in range(len(lpoints)):
        if (lpoints[i] in best_left) and (rpoints[i] in best_right):
            counter += 1
    return counter


def find_contours(img_name, threshold, thr_reset):
    img = cv2.imread(img_name)
    img = cv2.resize(img, (1920, 1080))
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
    rpoints = []
    for c in contours:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 1000 or cv2.contourArea(c) > 40000:
            continue

        # get the min area rect
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # draw a red box
        cv2.drawContours(img, [box], 0, (0, 0, 255), 2)

        # find the rect
        x, y, w, h = cv2.boundingRect(c)
        lpoints.append((x, y))
        rpoints.append((x + w, y))
        # lpoints.append(np.min(box, axis=0))
        # rpoints.append(np.min(box, axis=0))

    best_left = find_line(lpoints)
    best_right = find_line(rpoints)
    if best_right == None or best_left == None:
        return None
    right_line = linregress(best_right)
    left_line = linregress(best_left)
    if is_intersect(left_line, right_line) or check_lines(best_left, best_right, lpoints, rpoints) < 3:
        return None
    if not is_zebra(left_line, right_line):
        return None
    print_lines(img, right_line, left_line, best_left, best_right)
    return left_line, right_line


def print_lines(img, right_line, left_line, best_left, best_right):
    print("end")
    print("left line points")
    for point in best_left:
        print(point)
        cv2.circle(img, point, radius=5, color=(0, 0, 255), thickness=-1)
    print("right line points")
    for point in best_right:
        print(point)
        cv2.circle(img, point, radius=5, color=(0, 0, 255), thickness=-1)
    print("lines")
    print(left_line)
    print(right_line)
    cv2.line(img, right_line[0], right_line[1], (0, 0, 0), 9)
    cv2.line(img, left_line[0], left_line[1], (0, 0, 0), 9)
    # imS = cv2.resize(img, (960, 540))  # Resize image
    cv2.imshow("contours", img)
    key = cv2.waitKey(1000)


def check_image(img):
    counter = 0
    der = 0
    for i in range(120, 250, 10):
        for j in range(80, 100, 10):
            lines = find_contours(img, i, j)
            if lines is None:
                continue
            left_line, right_line = lines
            res = good_path(left_line, right_line)
            if res == 0:
                counter += 1
            else:
                der += res
                counter -= 1
    if counter > 0:
        print("ok")
    elif der < 0:
        print("left")
    else:
        print('right')


first = "img1.jpeg"
second = 'zebra.jpg'
No3 = 'zebra2.jpg'
No4 = 'rightView.jpg'
find_contours("zebra.jpg", 180, 255)
check_image(No4)
cv2.destroyAllWindows()
