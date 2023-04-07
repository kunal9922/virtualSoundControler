import cv2
import mediapipe
import numpy as np
import HandTracking as htm

#------------------ capturing frame size
wCam, hCam = 640, 480
#---------------------

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Hand tracking module 
detector = htm.HandDetector(detectionCon=0.7)

while True:
    success , img = cap.read()
    img = detector.findHands(img)
    #getting the list of detected hands landmakrs postion in pixels
    lmList = detector.findPosition(img, draw =False)
    if len(lmList):
        # 4 : THUMB_TIP,  8 : INDEX_FINGER_TIP
        print(lmList[4], lmList[8])
    

    cv2.imshow("Image basic", img)

    if cv2.waitKey(25) & 0xFF == ord('q'):                     
            break
    cv2.waitKey(1)
