import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture(0)
mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw = mp.solutions.drawing_utils

#Frame rates
pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    #Convert to rgb image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img)

    #checking weather hands are detecting 
    print(results.multi_hand_landmarks)
    #taking all hands to draw landmarks individually
    if results.multi_hand_landmarks:
       for handlms in results.multi_hand_landmarks:
          mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)
    #count frame rates 
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),3)

    cv2.imshow("Image", img)
    
    if cv2.waitKey(25) & 0xFF == ord('q'):                     
      break

    cv2.waitKey(1)

cv2.destroyAllWindows()
