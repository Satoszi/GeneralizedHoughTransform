import cv2
import numpy as np;

print("halo 1")
im = cv2.imread("blur8.jpg", cv2.IMREAD_GRAYSCALE)

detector = cv2.SimpleBlobDetector_create()
print("halo 2")

cv2.imshow("Keypoints", im)

cv2.waitKey(0)

keypoints = detector.detect(im)
print("halo 3")
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("Keypoints", im_with_keypoints)

cv2.waitKey(0)
