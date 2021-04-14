import math

import cv2

class Mapper:


    def __init__(self, img: str):
        self.img = img

    def getAnglesMap(self):
        anglesMap = []
        x_avg,y_avg = self.findCenter()
        #print("x = " + str(x_avg) + " y = " + str(y_avg))
        #img2 = self.img.copy()
        print("x = " + str(x_avg) + " y = " + str(y_avg) )
        for y in range (0, self.img.shape[0]):
            for x in range(0, self.img.shape[1]):
                if (self.img.item(y,x) == 255):

                    x_vector = x_avg - x
                    y_vector = y_avg - y

                    newImage = self.img.copy()
                    angle = self.calcEdgeAngle(newImage, x, y, 20)
                    angle_center = math.atan2(y_vector, x_vector)

                    distance = self.getDistance(x_avg, y_avg, x, y)
                    #print("x = " + str(x) + " y = " + str(y) + " angle_center = " + str(round(angle_center,2)) + " dist = " + str(round(distance,2)))
                    if (not (angle_center is None or distance is None or angle is None)):
                        anglesMap.append((angle_center,distance, angle))

                    #x2 = round(x + 50 * math.cos(angle-3.14))
                    #y2 = round(y + 50 * math.sin(angle-3.14))
                    #cv2.line(img2, (x,y), (x2,y2), (200), 1)

        #cv2.imshow("Image", img2)
        #cv2.waitKey(0)

        return anglesMap

    def findCenter(self):
        x_avg = 0
        y_avg = 0
        counter = 0

        for y in range (0, self.img.shape[0]):
            for x in range(0, self.img.shape[1]):
                if (self.img.item(y,x) == 255):
                    x_avg += x
                    y_avg += y
                    counter += 1
        x_avg /= counter
        y_avg /= counter

        return x_avg, y_avg

        #return cv2.circle(self.img, (int(x_avg), int(y_avg)), 20, (255, 0, 0), 3)

    def getDistance(self, x1, y1, x2, y2):
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return dist

    def trackEdge(self, image, tracked_point, x_start, y_start, r):
        x = tracked_point[0]
        y = tracked_point[1]
        image[y, x] = 254
        for i in range(-1 + y, 2 + y):
            for j in range(-1 + x, 2 + x):
                if not (i == y and j == x):
                    if 0 < i < image.shape[0] and 0 < j < image.shape[1] and image[i, j] == 255:
                        tracked_point[0] = j
                        tracked_point[1] = i

                        if self.getDistance(x_start, y_start, j, i) < r:
                            image[i, j] = 254
                            return self.trackEdge(image, tracked_point, x_start, y_start, r)
                        else:
                            return tracked_point.copy()

        return tracked_point.copy()

    def calcEdgeAngle(self, image, x, y, r):
        point = []
        image[y, x] = 254

        for i in range(-1 + y, 2 + y):
            for j in range(-1 + x, 2 + x):
                if (i > 0 and j > 0 and j < image.shape[1] and i < image.shape[0] and image[i, j] == 255):
                    neigh = []
                    neigh.append(j)
                    neigh.append(i)
                    point.append(neigh.copy())

        if len(point) < 2: return None

        point1 = self.trackEdge(image, point[0], x, y, r)
        point2 = self.trackEdge(image, point[1], x, y, r)

        x_vector = point1[0] - point2[0]
        y_vector = point1[1] - point2[1]

        return math.atan2(y_vector, x_vector)