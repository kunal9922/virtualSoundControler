import cv2
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
        #volume range from -65 to 0
        self.vol = 0
        

    def run(self, img):
        img = self.detector.findHands(img)
        lmList = self.detector.findPosition(img, draw=False)
        # store the volume percentage 
        volPer = 0
        # pixel locations of the thumb tip and Index Finger
        x1 = y1 = x2 = y2 = None
        if len(lmList):
            x1, y1 = lmList[4][1], lmList[4][2]  # Thumb Tip
            x2, y2 = lmList[8][1], lmList[8][2]  # Index FInger Tip
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cx, cy = (x1+x2)//2, (y1+y2)//2
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)
            length = math.hypot(x2 -x1, y2 - y1)
            self.vol = np.interp(length, [40, 200], [self.minVol, self.maxVol])
            self.volume.SetMasterVolumeLevel(self.vol, None)
            # converting the volume ranges from 0 to 100 as percentage
            volPer = np.interp(length, [40, 200], [0, 100])
            if length < 40:
                cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)

        return img, volPer, lmList, ((x1, y1), (x2, y2)) # thumb and index finger tuple

    def release(self):
       # self.cap.release()
        cv2.destroyAllWindows()

# wCam, hCam = 640, 480
# hand_volume_control = HandVolumeControl(wCam, hCam)
# hand_volume_control.run()
# hand_volume_control.release()
