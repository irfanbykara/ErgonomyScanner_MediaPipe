import cv2
import mediapipe as mp
import time
import imutils
import pyautogui
import datetime
import PoseDetector


def getDif(posNose,posFin):
    if posNose!=None and posFin!=None:
        posNoseX = posNose[1]
        posNoseY = posNose[2]
        posFinX = posFin[1]
        posFinY = posFin[2]
        dist = ((posNoseX-posFinX)**2+(posNoseY-posFinY)**2)**0.5

        return dist

def onClick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        total_time = param[0] + param[1]
        danger_time = param[1]
        print(str("%.2f" % (danger_time/total_time))+ ' the danger zone working rate...')

def main():

    start_time = datetime.datetime.now()
    st_millisecond = start_time.timestamp()
    cap = cv2.VideoCapture( 0 )
    pTime = 0
    detector = PoseDetector.PoseDetectorClass()
    safe_counter = 0
    danger_counter = 0

    while True:

        success, img = cap.read()

        img = detector.findPose(img)
        lmList = detector.getPos(img)

        try:
            difEye = getDif(lmList[2],lmList[19])
            difWrist = getDif(lmList[15],lmList[19])
            difShoulders = getDif( lmList[11], lmList[12] )

            if difWrist<=difShoulders/3-17:
                cv2.rectangle( img, (50, 100), (100, 150), (0, 0, 255), -1 )

                current_time = datetime.datetime.now()
                ct_millisecond = current_time.timestamp()
                if abs(ct_millisecond-st_millisecond)>10:
                    pyautogui.screenshot( "resources/screenshot{}.png".format(str(danger_counter)) )
                    st_millisecond = ct_millisecond
                danger_counter += 1
            else:
                cv2.rectangle( img, (50, 100), (100, 150), (0, 255, 0), -1 )

                safe_counter += 1
        except:
            pass
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.namedWindow( "Webcam" )

        cv2.putText( img, 'FPS: '+str( int( fps ) ),
                     (50, 50),
                     cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3 )
        cv2.rectangle(img, (400,400),(200,350),(0,0,255),-1)
        cv2.putText( img, str( 'Report' ),
                     (215, 390),
                     cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3 )
        cv2.setMouseCallback('Webcam',onClick,param=[safe_counter,danger_counter])
        cv2.imshow( 'Webcam', img )

        cv2.waitKey( 1 )


if __name__ == "__main__":
    main()