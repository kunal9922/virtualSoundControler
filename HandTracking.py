import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()

    cv2.imshow("Image", img)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):                     
      break

    cv2.waitKey(1)

cv2.destroyAllWindows()
