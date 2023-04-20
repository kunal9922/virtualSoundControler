import cv2
import mediapipe
import numpy as np
import HandTracking as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

class HandVolumeControl:
    def __init__(self, wCam, hCam):
       # self.cap = cv2.VideoCapture(0)
        # self.cap.set(3, wCam)
        # self.cap.set(4, hCam)
        self.detector = htm.HandDetector(detectionCon=0.7)
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        volRange = self.volume.GetVolumeRange()
        self.minVol = volRange[0]
        self.maxVol = volRange[1]

    def run(self, img):
        img = self.detector.findHands(img)
        lmList = self.detector.findPosition(img, draw=False)
        if len(lmList):
            x1, y1 = lmList[4][1], lmList[4][2]  
            x2, y2 = lmList[8][1], lmList[8][2]  
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cx, cy = (x1+x2)//2, (y1+y2)//2
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)
            length = math.hypot(x2 -x1, y2 - y1)

            vol = np.interp(length, [40, 200], [self.minVol, self.maxVol])
            self.volume.SetMasterVolumeLevel(vol, None)

            if length < 40:
                cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)

        return img 

    def release(self):
       # self.cap.release()
        cv2.destroyAllWindows()

# wCam, hCam = 640, 480
# hand_volume_control = HandVolumeControl(wCam, hCam)
# hand_volume_control.run()
# hand_volume_control.release()
