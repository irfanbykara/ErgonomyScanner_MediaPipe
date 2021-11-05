import cv2
import mediapipe as mp
import time
import imutils
import pyautogui
import datetime
import csv
import PoseDetector
import numpy as np
import pafy
import youtube_dl

# This project is written by Irfan Baykara. It serves as a labeling program that one can label positive and negative postures of people in a specific video.
# Press down the 'n' key for negative actions in the video, and 'p' key for the positive actions. This dataset can be fed into a neural net in the future.

def main():
    url = "https://www.youtube.com/watch?v=nm-fxV-bwWg"
    video = pafy.new( url )
    best = video.getbest( preftype="mp4" )

    cap = cv2.VideoCapture()  # Youtube
    cap.open( best.url )

    detector = PoseDetector.PoseDetectorClass()


    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPos(img)
        if cv2.waitKey( 33 ) == ord( 'n' ):
            cv2.rectangle(img, (50, 100), (100, 150), (0, 0, 255), -1)
            main_list = []
            for i in lmList:

                main_list.append(float(i[1]))
                main_list.append(float(i[2]))

            main_list.append('Neg')
            with open('ergonomy_dataset.csv', 'a', newline='') as myfile:
                wr = csv.writer( myfile, delimiter = ',')
                wr.writerow(main_list)
        elif cv2.waitKey( 33 ) == ord( 'p' ):
            cv2.rectangle(img, (50, 100), (100, 150), (0, 255, 0), -1)
            main_list = []
            for i in lmList:
                main_list.append( float(i[1] ))
                main_list.append( float(i[2] ))

            main_list.append( 'Pos' )

            with open( 'ergonomy_dataset.csv', 'a', newline='' ) as myfile:
                wr = csv.writer( myfile, delimiter = ',')
                wr.writerow( main_list )
        cv2.imshow( 'Webcam', img )

        cv2.waitKey( 1 )
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()