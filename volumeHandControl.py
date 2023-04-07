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
        # creating circles over the 4 : THUMB_TIP,  8 : INDEX_FINGER_TIP
        x1, y1 = lmList[4][1], lmList[4][2]  # 4 : THUMB_TIP
        x2, y2 = lmList[8][1], lmList[8][2]  # 8 : INDEX_FINGER_TIP
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)

        # creating a line btw 4 : THUMB_TIP AND 8 : INDEX_FINGER_TIP
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)


    

    cv2.imshow("Image basic", img)

    if cv2.waitKey(25) & 0xFF == ord('q'):                     
            break
    cv2.waitKey(1)
