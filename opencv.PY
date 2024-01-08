import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
from PIL import Image
import os
#def scan_plate():   
print(cv2. __version__)
reader = easyocr.Reader(['en'])

img = cv2.imread('image14.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
#("gray",gray)
# cv2.waitKey(0)
bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
edged = cv2.Canny(bfilter, 50, 250) #Edge detection
plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
#("edged",edged)
# print(reader.readtext(edged))
# cv2.waitKey(0)
keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
location = None
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, True)
    if len(approx) == 4:
        location = approx
        break
print(location)
mask = np.zeros(gray.shape, np.uint8)
new_image = cv2.drawContours(mask, [location], 0,255, -1)
new_image = cv2.bitwise_and(img, img, mask=mask)
plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
#("new img",new_image)
# cv2.waitKey(0)
(x,y) = np.where(mask==255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
cropped_image = gray[x1:x2+1, y1:y2+1]
plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
#("cropped",cropped_image)
# cv2.waitKey(0)
#reader = easyocr.Reader(['en'])
result = reader.readtext(cropped_image)
print(result)
#return result
#[([[11, 5], [494, 5], [494, 126], [11, 126]], 'AN-684FH', 0.6564995730215452)]
#[([[9, 0], [547, 0], [547, 181], [9, 181]], 'AG-963-SR', 0.6864369628987527)]