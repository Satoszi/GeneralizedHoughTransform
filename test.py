from CircleMake import CircleMake
from Mapper import Mapper
import cv2
import math

print(math.atan2(-34,-23)*57.3)


pattern = "pattern1.jpg"
file2 = "recog1.jpg"

Image = cv2.imread(pattern)
window_name = "Image"
gray = cv2.cvtColor(Image, cv2.COLOR_BGR2GRAY)


val1 = 100
val2 = 100
gray = cv2.Canny(gray, val1, val2)

cv2.imshow("Image", gray)
cv2.waitKey(100)

asd = Mapper(gray)
mapa = asd.getAnglesMap()
#print(mapa)
print(len(mapa))
a = CircleMake()
a.main(mapa, file2)

