import cv2
import mediapipe as mp
import time
import imutils
import pyautogui
import datetime
import pose_detector
import scanner
import pafy

def onClick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        total_time = param[0] + param[1]
        danger_time = param[1]
        print( str( "%.2f" % (danger_time / total_time) ) + ' the danger zone working rate...' )


def main():
    url = "https://www.youtube.com/watch?v=WZRJW4UpkkE"
    video = pafy.new( url )
    best = video.getbest( preftype="mp4" )

    cap = cv2.VideoCapture()  # Youtube
    cap.open( best.url )

    start_time = datetime.datetime.now()
    st_millisecond = start_time.timestamp()
    # cap = cv2.VideoCapture( 0 )
    pTime = 0
    detector = pose_detector.PoseDetectorClass()
    safe_counter = 0
    danger_counter = 0

    while True:

        success, img = cap.read()

        img = detector.findPose( img )
        lmList = detector.getPos( img )
        scanner_ = scanner.ScanErgonomy( lmList )

        if lmList:

            if scanner_.ergonomy_checker() == False:
                cv2.rectangle( img, (50, 100), (100, 150), (0, 0, 255), -1 )

                current_time = datetime.datetime.now()
                ct_millisecond = current_time.timestamp()
                if abs( ct_millisecond - st_millisecond ) > 15:
                    pyautogui.screenshot( "resources/screenshot{}.png".format( str( danger_counter ) ) )
                    st_millisecond = ct_millisecond
                danger_counter += 1
            else:
                cv2.rectangle( img, (50, 100), (100, 150), (0, 255, 0), -1 )

                safe_counter += 1

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.namedWindow( "Ergonomy Checker" )

        cv2.putText( img, 'FPS: ' + str( int( fps ) ),
                     (50, 50),
                     cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3 )
        cv2.setMouseCallback( 'Ergonomy Checker', onClick, param=[safe_counter, danger_counter] )
        cv2.imshow( 'Ergonomy Checker', img )

        cv2.waitKey( 1 )


if __name__ == '__main__':
    main()
