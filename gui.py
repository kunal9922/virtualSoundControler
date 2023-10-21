import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from volumeHandControl import HandVolumeControl 
import numpy as np

class Icon:
    def __init__(self, imgPath, *imgSize: list):
        self.imgPath = imgPath
        # Load the icon image
        icon_image = cv2.imread(self.imgPath)

        if imgSize:
            self.row, self.col = imgSize[0]
            icon_image = cv2.resize(icon_image, (self.row, self.col))  # Resize the image if needed

        icon_image = cv2.cvtColor(icon_image, cv2.COLOR_BGR2RGB)
        icon_image = Image.fromarray(icon_image)  # Replace "icon.png" with the path to your icon image
        
        # Create a Tkinter-compatible image
        self.icon = ImageTk.PhotoImage(icon_image)




#toggle switch to turn ON and turn OFF hand detection 
def detectToggle():
    global detectHand, app
    if app.hd_toggle_button.config('text')[-1] == "Hand Detection OFF":
        app.hd_toggle_button.config(text="Hand Detection ON", image = app.hndOn, compound= 'left', style='Blue.TButton' )
        detectHand = True
    else:
        app.hd_toggle_button.config(text="Hand Detection OFF", image = app.hndOFF, compound= 'left', style='Blue.TButton')
        detectHand = False


# Function to open the camera
def open_camera():
    global cap
    cap = cv2.VideoCapture(0)
    # Set camera resolution to lower value for faster processing
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Function to close the camera
def close_camera():
    global cap, app
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()
        cap = None
        # Convert frame to ImageTk.PhotoImage object
        imgBlank = np.zeros((480,640), np.int8)
        img = Image.fromarray(imgBlank)
        img_tk = ImageTk.PhotoImage(image=img)
        # Update label with new frame
        app.label.config(image=img_tk)
        app.label.image = img_tk

# Function to update the camera frame in the GUI
def update_frame():
    global hand_volume_control, app

    if cap is not None:
        ret, frame = cap.read()
        # Apply Gaussian blur to the entire frame
        blurred_frame = cv2.GaussianBlur(frame, (99, 99), 0)
        if ret:
            if detectHand is not False:
                frame, vol, landmarks, thumb_index = hand_volume_control.run(frame)
                app.scaleValue.set(vol)

                # Get the landmarks for the first hand and create a hand mask
                hand_mask = np.zeros_like(frame[:, :, 0], dtype=np.uint8)
                # Set hand landmarks to white in the hand mask
                for lm in landmarks:
                    id, cx, cy = lm
                    cv2.circle(hand_mask, (cx, cy), 5, (255), cv2.FILLED)
                # Apply Gaussian blur to the entire frame
                blurred_frame = cv2.GaussianBlur(frame, (99, 99), 0)

                # Invert the hand mask to create a background mask
                background_mask = cv2.bitwise_not(hand_mask)

                # Apply the background mask to the blurred frame
                blurred_background = cv2.bitwise_and(blurred_frame, blurred_frame, mask=background_mask)

                # Apply the hand mask to the original frame to keep the hand focused
                focused_hand = cv2.bitwise_and(frame, frame, mask=hand_mask)

                # Combine the focused hand and blurred background
                frame = cv2.add(focused_hand, blurred_background)
                
                # Draw lines connecting finger landmarks to create a palm structure
                if len(landmarks) >= 21:
                    fingers = [[0, 1, 2, 3, 4], [0, 5, 6, 7, 8], [0, 9, 10, 11, 12], [0, 13, 14, 15, 16], [0, 17, 18, 19, 20]]
                    for finger in fingers:
                        for i in range(len(finger) - 1):
                            cv2.line(frame, tuple(landmarks[finger[i]][1:]), tuple(landmarks[finger[i + 1]][1:]), (0, 255, 0), 2)
                    # Draw a line between thumb and index finger to recognize the volume levels
                    cv2.line(frame, thumb_index[0], thumb_index[1], (0, 255, 0), 3)
                
                #Set the new hand detected frame with blur effect
                blurred_frame = frame 
            # Convert frame from BGR to RGB
            frame_rgb = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2RGB)
            # Convert frame to ImageTk.PhotoImage object
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)
            # Update label with new frame
            app.label.config(image=img_tk)
            app.label.image = img_tk
            
    # Schedule next frame update after 5 ms
    app.label.after(5, update_frame)

class windowGui:
    def __init__(self):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("Wireless Sound Control System")
        ico = Image.open(r'dataset\\magicHands.png')
        photo = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, photo)

    def exe(self):
        #icon hand detection icon On and OFF
        self.hndOn = Icon(r'dataset\\palmDetection.png', (50, 50))
        self.hndOn = self.hndOn.icon
        self.hndOFF = Icon(r'dataset\\palmDetectionBlock.png', (50, 50))
        self.hndOFF = self.hndOFF.icon

        #Icon camera open and close
        self.camOpen = Icon(r'dataset\\iconCam.png', (50, 50))
        self.camOpen = self.camOpen.icon
        self.camClose = Icon(r'dataset\\closeCam2.png',(50, 50))
        self.camClose = self.camClose.icon

        
        # Create a frame to hold the camera frame label
        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=10)

        # Create a label to display the camera frame
        self.label = ttk.Label(self.frame)
        self.label.pack()

        # Create "Open Camera" button
        self.open_button = ttk.Button(self.root, text="Open Camera", image=self.camOpen, command=open_camera, compound= 'left', style='Blue.TButton' )
        self.open_button.pack(pady=5)

        # Create "Close Camera" button
        self.close_button = ttk.Button(self.root, text="Close Camera", image=self.camClose, command=close_camera, compound= 'left', style='Blue.TButton')
        self.close_button.pack(pady=5)

        # Create " Hand detection " toggle button
        self.hd_toggle_button = ttk.Button(self.root, text="Hand Detection ON",image=self.hndOn, command= detectToggle, compound= 'left', style='Blue.TButton')
        self.hd_toggle_button.pack(pady=5)

        #slider that shows the current volume by changing hand gestures.
        self.scaleValue = tk.IntVar()
        slider = ttk.Scale(
            self.root,
            from_=0,
            to=100,
            orient='horizontal',
            variable= self.scaleValue
        )


        # Apply some styling to the buttons
        self.style = ttk.Style()
        self.style.configure("TButton", padding=10, font=("Helvetica", 12))


        # Start updating frames
        update_frame()

        # Run the GUI event loop
        self.root.mainloop()

# by default detection is True 
detectHand = True

# OpenCV VideoCapture object for camera input
cap = cv2.VideoCapture(0)
# Set camera resolution to lower value for faster processing
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
hand_volume_control = HandVolumeControl(640, 480)

def exe():
    app = windowGui()
    # Set the local variable as global
    globals()["app"] = app
    app.exe()
    