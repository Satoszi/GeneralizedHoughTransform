import cv2
import numpy as np
import math


class EdgeAngleCalculator:

    def __init__(self):
        pass

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
