import cv2
import mediapipe
import numpy as np
import HandTracking as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

#------------------ capturing frame size
wCam, hCam = 640, 480
#---------------------

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# Hand tracking module 
detector = htm.HandDetector(detectionCon=0.7)

# control volume library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# get the range of volume which goes (min -65.25 to max 0.0) 
volRange = volume.GetVolumeRange()

minVol = volRange[0]
maxVol = volRange[1]

while True:
    success , img = cap.read()
    img = detector.findHands(img)
    #getting the list of detected hands landmakrs postion in pixels
    lmList = detector.findPosition(img, draw =False)
    if len(lmList):
        # 4 : THUMB_TIP,  8 : INDEX_FINGER_TIP
        # print(lmList[4], lmList[8])
        # creating circles over the 4 : THUMB_TIP,  8 : INDEX_FINGER_TIP
        x1, y1 = lmList[4][1], lmList[4][2]  # 4 : THUMB_TIP
        x2, y2 = lmList[8][1], lmList[8][2]  # 8 : INDEX_FINGER_TIP
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cx, cy = (x1+x2)//2, (y1+y2)//2
        # creating a line btw 4 : THUMB_TIP AND 8 : INDEX_FINGER_TIP
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)
        lenght = math.hypot(x2 -x1, y2 - y1)
       


        #hand range 10 - 300
        #volume range -65 -0
        '''Now converting the volume range according to pixel line range'''
        vol = np.interp(lenght, [40, 200], [minVol, maxVol])
        print(int(lenght), vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        if lenght < 50:
             cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)


    cv2.imshow("Image basic", img)

    if cv2.waitKey(25) & 0xFF == ord('q'):                     
            break
    cv2.waitKey(1)
