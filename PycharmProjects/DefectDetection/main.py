import cv2
import numpy as np

def dummy(val):
    pass

path = "resources/passat.jfif"
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640,240)
cv2.createTrackbar("Hue Min","TrackBars", 79, 179, dummy )
cv2.createTrackbar("Hue Max","TrackBars", 169, 179, dummy )
cv2.createTrackbar("Sat Min","TrackBars", 79, 255, dummy )
cv2.createTrackbar("Sat Max","TrackBars", 255, 255, dummy )
cv2.createTrackbar("Val Min","TrackBars", 30, 255, dummy )
cv2.createTrackbar("Val Max","TrackBars", 255, 255, dummy )
while True:
    img = cv2.imread(path)
    img = cv2.resize( img, (700, 400) )





    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imgGRAY = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max","TrackBars")
    sat_min = cv2.getTrackbarPos("Sat Min","TrackBars")
    sat_max = cv2.getTrackbarPos("Sat Max","TrackBars")
    val_min = cv2.getTrackbarPos("Val Min","TrackBars")
    val_max = cv2.getTrackbarPos("Val Max","TrackBars")
    print(h_min,h_max,sat_min,sat_max,val_min,val_max)
    lower = np.array([h_min,sat_min,val_min])
    upper = np.array( [h_max, sat_max, val_max] )
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)

    cv2.imshow('Final', imgResult)
    cv2.waitKey(1)

