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




#toggle switch to Trun ON and Trun OFF hand detection 
def detectToggle():
    global detectHand, app
    if app.hd_toggle_button.config('text')[-1] == "OFF":
        app.hd_toggle_button.config(text="ON", image = app.hndOn, compound= tk.RIGHT )
        detectHand = True
    else:
        app.hd_toggle_button.config(text="OFF", image = app.hndOFF, compound= tk.RIGHT )
        detectHand = False


# Function to open the camera
def open_camera():
    global cap
    cap = cv2.VideoCapture(0)

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
        if ret:
            if detectHand is not False:
                frame, vol = hand_volume_control.run(frame)
                app.scaleValue.set(vol)
                
            # Convert frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Resize frame to fit in GUI window
            frame_rgb = cv2.resize(frame_rgb, (640, 480))
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
        ico = Image.open('./dataset/magicHands.png')
        photo = ImageTk.PhotoImage(ico)
        self.root.wm_iconphoto(False, photo)

    def exe(self):
        #icon hand detection icon On and OFF
        self.hndOn = Icon(r'./dataset/toggleON.png', (50, 50))
        self.hndOn = self.hndOn.icon
        self.hndOFF = Icon(r'./dataset/toggleOFF.png', (50, 50))
        self.hndOFF = self.hndOFF.icon

        
        # Create a frame to hold the camera frame label
        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=10)

        # Create a label to display the camera frame
        self.label = ttk.Label(self.frame)
        self.label.pack()

        # Create "Open Camera" button
        self.open_button = ttk.Button(self.root, text="Open Camera", command=open_camera)
        self.open_button.pack(pady=5)

        # Create "Close Camera" button
        self.close_button = ttk.Button(self.root, text="Close Camera", command=close_camera)
        self.close_button.pack(pady=5)

        # Create " Hand detection " toggle button
        self.hd_toggle_button = ttk.Button(self.root, text="ON",image=self.hndOn, command= detectToggle)
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
hand_volume_control = HandVolumeControl(640, 480)

def exe():
    app = windowGui()
    # Set the local variable as global
    globals()["app"] = app
    app.exe()
    