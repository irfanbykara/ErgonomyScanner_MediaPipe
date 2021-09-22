import numpy as np
import cv2
import math
import pytesseract
from scipy import ndimage
import builtins


original_open = open
def bin_open(filename, mode='rb'):
    return original_open(filename, mode)

IMAGE_FILE_LOCATION = "resources/text.png" # Any random text
input_img = cv2.imread(IMAGE_FILE_LOCATION) # Reading image

global degree
degree=0
global coordinatesList

coordinatesList = []


def orientation_correction(img, save_image=False):
    img_gray = cv2.cvtColor( img, cv2.COLOR_BGR2GRAY )
    img_edges = cv2.Canny( img_gray, 100, 100, apertureSize=3 )
    lines = cv2.HoughLinesP( img_edges, 1, math.pi / 180.0, 100, minLineLength=100, maxLineGap=5 )

    angles = []
    for x1, y1, x2, y2 in lines[0]:
        angle = math.degrees( math.atan2( y2 - y1, x2 - x1 ) )
        angles.append( angle )

    median_angle = np.median( angles )

    img_rotated = ndimage.rotate( img, median_angle )

    if save_image:
        cv2.imwrite( 'orientation_corrected.jpg', img_rotated )
    return img_rotated



img_rotated = orientation_correction( input_img )
coordinates = []


def shape_selection(event, x, y, flags, param):
    global coordinates
    global coordinatesList
    global degree
    if event == cv2.EVENT_LBUTTONDOWN:
        coordinatesList.append((x,y))
        coordinates = [(x, y)]
    elif event == cv2.EVENT_LBUTTONUP:
        coordinates.append( (x, y) )

        coordinatesList.append( (x, y))
        cv2.rectangle( image, coordinates[0], coordinates[1], (0, 0, 255),2)
        textCoordinatesX =coordinates[0][0]-20
        textCoordinatesY = int((coordinates[0][1] + coordinates[1][1])/2)
        degree=degree+1
        cv2.circle(image,(textCoordinatesX+7,textCoordinatesY-7),10,color=(0,0,255),thickness=20)
        cv2.putText(image,str(degree),(textCoordinatesX,textCoordinatesY),cv2.FONT_HERSHEY_DUPLEX,fontScale=1,color=(0,0,0),lineType=10)
        cv2.imshow( "image", image )



image = img_rotated

image_copy = image.copy()
cv2.namedWindow( "image" )
cv2.setMouseCallback( "image", shape_selection )

while True:

    cv2.imshow( "image", image )
    key = cv2.waitKey( 1 ) & 0xFF

    if key == 13:  # If 'enter' is pressed, apply OCR
        break

    if key == ord( "c" ):  # Clear the selection when 'c' is pressed
        degree=0
        counter =0
        coordinatesList=[]
        image = image_copy.copy()

counter = 0
for coors in range(int(len(coordinatesList)/2)):
    if(len(coordinatesList[coors])==2):
        image_roi = image_copy[coordinatesList[counter][1]:coordinatesList[counter+1][1],
                    coordinatesList[counter][0]:coordinatesList[counter+1][0]]
        counter+=2
        pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
        text = pytesseract.image_to_string( image_roi,
                                            )

        with open("output_ocr", 'a', encoding='utf-8') as f:

           f.writelines(text.split("\n")[0])
           f.writelines("\n")

        print( text.split("\n")[0])

cv2.destroyAllWindows()

