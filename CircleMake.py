import time

import cv2
import numpy as np
import math


class CircleMake:

    def __init__(self):
        self.regeneratePixels = []
        self.tracking = 0
        self.listing = 0
        self.edging = 0

    def getDistance(self, x1, y1, x2, y2):
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist

    def trackEdge(self, image, tracked_point, x_start, y_start, r):
        x = tracked_point[0]
        y = tracked_point[1]
        image.itemset(y, x,249)
        self.regeneratePixels.append((y,x))
        for i in range(-1 + y, 2 + y):
            for j in range(-1 + x, 2 + x):
                if not (i == y and j == x):
                    if 0 < i < image.shape[0] and 0 < j < image.shape[1] and image.item(i, j) >= 252:
                        tracked_point[0] = j
                        tracked_point[1] = i

                        if self.getDistance(x_start, y_start, j, i) < r:
                            image.itemset(y, x,249)
                            self.regeneratePixels.append((i, j))
                            return self.trackEdge(image, tracked_point, x_start, y_start, r)
                        else:
                            return tracked_point.copy()

        return tracked_point.copy()

    def calcEdgeAngle(self, image, x, y, r):
        point = []
        self.regeneratePixels.clear()

        image.itemset(y, x,249)
        self.regeneratePixels.append((y, x))

        for i in range(-1 + y, 2 + y):
            for j in range(-1 + x, 2 + x):
                if (i > 0 and j > 0 and j < image.shape[1] and i < image.shape[0] and image.item(i, j) >= 252):
                    neigh = []
                    neigh.append(j)
                    neigh.append(i)
                    point.append(neigh.copy())

        if len(point) < 2: return None

        point1 = self.trackEdge(image, point[0], x, y, r)
        point2 = self.trackEdge(image, point[1], x, y, r)

        for elem in self.regeneratePixels:
            image.itemset(elem[0],elem[1], 255)

        x_vector = point1[0] - point2[0]
        y_vector = point1[1] - point2[1]

        return math.atan2(y_vector, x_vector)


    def shoreCond(self, y, x, height, width):
        if y < 0: return False
        if y >= height: return False
        if x < 0: return False
        if x >= width: return False
        return True


    def drawHoughSpaceForCircle(self, Image, anglesList, scale):
        gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
        gray = cv2.Canny(gray, 70, 70);
        #cv2.imshow("Image", gray)
        #cv2.waitKey(100)

        height = gray.shape[1]
        width = gray.shape[0]
        zeros = []
        houghSpace = []

        depth = 80

        for i in range (0,depth):
            zeros.append([ [0] * height for _ in range(width)])
            houghSpace.append(gray.copy())

        print("STARTE")
        start = time.time()

        for start_y in range(0, gray.shape[0], 1):
            for start_x in range(0, gray.shape[1], 1):
                if gray.item(start_y,start_x) == 255:

                    #newImage = gray.copy()
                    angle = self.calcEdgeAngle(gray, start_x, start_y,20)

                    if (not angle is None):
                        #for angleDistancePair in anglesList:
                        for i in range (0, len(anglesList), 15):
                            angleDistancePair = anglesList[i]
                            additional_agnle = angleDistancePair[0]


                            radius = angleDistancePair[1]
                            angle_to_eq = angleDistancePair[2]
                            additional = angle_to_eq - angle

                            dimens = int(1.6*(additional+3.142)*depth/10)
                            if dimens > depth-1: dimens = depth-1
                            if dimens < 0: dimens = 0

                            #if abs((angle - angle_to_eq)) < 0.1:
                            if 1 == 1:
                                x2 = int(start_x + radius * math.cos(additional_agnle - additional))
                                y2 = int(start_y + radius * math.sin(additional_agnle - additional))


                                for i in range(-2, 3):
                                    for j in range(-2, 3):
                                        if self.shoreCond(y2 + i, x2 + j, width, height):
                                            if (zeros[dimens][y2 + i][x2 + j] < 254):
                                                zeros[dimens][y2 + i][x2 + j] += 2


        end = time.time()
        print(end - start)
        print("STOPE")

        Image2d = gray.copy()
        for start_y in range(0, gray.shape[0], 1):
            for start_x in range(0, gray.shape[1], 1):
                Image2d.itemset(start_y, start_x, 0)

        for dim in range (2,depth-2):
            for start_y in range(0, gray.shape[0], 1):
                for start_x in range(0, gray.shape[1], 1):
                    Image2d.itemset(start_y,start_x, Image2d.item(start_y,start_x) + zeros[dim][start_y][start_x]**1.7/25)
            cv2.imshow("Image", Image2d)
            cv2.waitKey(10)
        cv2.waitKey(10000)

        for dim in range (0,depth):
            for start_y in range(0, gray.shape[0], 1):
                for start_x in range(0, gray.shape[1], 1):
                    houghSpace[dim].itemset(start_y,start_x,zeros[dim][start_y][start_x])
            cv2.imshow("Image", houghSpace[dim])
            cv2.waitKey(1)

        while True:
            for dim in range(2, depth-2):
                cv2.imshow("Image", houghSpace[dim])
                cv2.waitKey(30)

        return houghSpace[0]

    # Searching blobs in Hough Space
    def getcirclesCenter(self, houghSpace):
        kernel_size = 20
        kernel = cv2.getStructuringElement(0, ksize=(kernel_size, kernel_size))
        houghSpace = cv2.morphologyEx(houghSpace, 3, kernel)

        kernel_size = 10
        kernel = cv2.getStructuringElement(0, ksize=(kernel_size, kernel_size))
        houghSpace = cv2.morphologyEx(houghSpace, 5, kernel)

        pointList = []
        ret, thresh = cv2.threshold(houghSpace, 60, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            M = cv2.moments(c)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                point = []
                point.append(cX)
                point.append(cY)

                pointList.append(point.copy())

        return pointList


    def main(self, anglesList, file):


        Image = cv2.imread(file)

        cv2.imshow("Image", Image)
        cv2.waitKey(100)

        radius = 30
        scale = 1
        # Drawing Hough Space for circles where r = 30px
        houghSpace = self.drawHoughSpaceForCircle(Image,anglesList, scale)

        # Searching Blobs in the Hough space
        circlesCenter = self.getcirclesCenter(houghSpace)

        # Drawing Circles
        for circlePoint in circlesCenter:
            cv2.circle(Image, (circlePoint[0], circlePoint[1]), 30, (0, 255, 0), 2)

        cv2.imshow("Image", Image)
        cv2.imshow("Image1", houghSpace)
        cv2.waitKey(0)
