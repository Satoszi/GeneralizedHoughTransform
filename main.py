from __future__ import print_function
import cv2
import argparse

import numpy as np

val1 = 100
val2 = 200


def onTrackbar1(val):
    global val1
    val1 = val


def onTrackbar1(val):
    global val2
    val2 = val


file = "blur6.jpg"
Image = cv2.imread(file)

window_name = "Image"
# cv2.imshow(window_name, Image)
cv2.createTrackbar("Min Threshold:1", window_name, 10, 100, onTrackbar1)
cv2.createTrackbar('Min Threshold:2', window_name, 10, 100, onTrackbar1)

gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)
data = np.asarray(gray.copy())
gray.put
print(gray.shape[1] / 2)
print(gray.shape[0] / 2)

tab = []
for i in range (0,1000):
    tab.append(i)
tab2 = []
for i in range (0,1000):
    tab2.append(tab.copy())
a = 4
for counter in range(0, 1000):
    print(counter)
    for i in range(0, 1000000):

            a = a + 3
            #value = data.item(i,j)
            #value += int((255-value)/10)
            #data.itemset(i, j, value)
    cv2.imshow("Image", data)
    cv2.waitKey(5)

print(val1)