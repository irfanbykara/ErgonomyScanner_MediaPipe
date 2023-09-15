import cv2
import mediapipe as mp
class PoseDetectorClass():

    def __init__(self,mode=False, upBody = False, smooth =True,
                 detectionCon = 0.5, trackCon = 0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.holistic
        self.pose = self.mpPose.Holistic()

    def findPose(self, img, draw = True):

        imgRGB = cv2.cvtColor( img, cv2.COLOR_BGR2RGB )
        self.results = self.pose.process( imgRGB )
        if self.results.pose_landmarks:

            if draw:
                self.mpDraw.draw_landmarks( img, self.results.pose_landmarks,
                                       self.mpPose.POSE_CONNECTIONS )
                for id, lm in enumerate( self.results.pose_landmarks.landmark ):
                    h, w, c = img.shape
                    cx, cy = int( lm.x * w ), int( lm.y * h )

                    cv2.circle( img, (cx,cy), 5, (255, 255, 255), cv2.FILLED )
        return img

    def getPos(self,img,draw=True):
        lmList = []
        if self.results.pose_landmarks:

            for id, lm in enumerate( self.results.pose_landmarks.landmark ):
                h, w, c = img.shape
                cx, cy = int( lm.x * w ), int( lm.y * h )
                lmList.append([id,cx,cy])

                cv2.circle( img, (lmList[0][0],lmList[0][1]), 20, (255, 255, 255), cv2.FILLED )
        return lmList
