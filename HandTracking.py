import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5) -> None:
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
               
        self.hands = self.mpHands.Hands(static_image_mode= self.mode, max_num_hands= self.maxHands,
                                        min_detection_confidence= self.detectionCon, min_tracking_confidence= self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        

    def findHands(self, img, draw=True):
        #Convert to rgb image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        #taking all hands to draw landmarks individually
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw = False):
        lmList = []
        #finding out each landmarks of tracked hand
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm, in enumerate(hand.landmark):
                h, w, c = img.shape
                # we have only decimal values of landmark
                #to convert it into pixel (landmark.x * widthOfImage) and so on
                cx, cy = int(lm.x * w) , int(lm.y * h)
                #print(id, cx, cy)
                lmList.append([id,cx,cy])

                #draw cricle on the detected landmarks on the hand
                if draw == True:
                    cv2.circle(img, (cx,cy), 15, (0,0,255), cv2.FILLED)
        
        return lmList