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

# Create the main window
root = tk.Tk()
root.title("Wireless Sound Control System")
ico = Image.open('./dataset/magicHands.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)


# OpenCV VideoCapture object for camera input
cap = cv2.VideoCapture(0)
hand_volume_control = HandVolumeControl(640, 480)

# by default detection is True 
detectHand = True

#icon hand detection icon On and OFF
hndOn = Icon(r'./dataset/toggleON.png', (50, 50))
hndOn = hndOn.icon
hndOFF = Icon(r'./dataset/toggleOFF.png', (50, 50))
hndOFF = hndOFF.icon


#toggle switch to Trun ON and Trun OFF hand detection 
def detectToggle():
    global detectHand
    if hd_toggle_button.config('text')[-1] == "OFF":
        hd_toggle_button.config(text="ON", image = hndOn, compound= tk.RIGHT )
        detectHand = True
    else:
        hd_toggle_button.config(text="OFF", image = hndOFF, compound= tk.RIGHT )
        detectHand = False


# Function to open the camera
def open_camera():
    global cap
    cap = cv2.VideoCapture(0)

# Function to close the camera
def close_camera():
    global cap
    if cap is not None:
        cap.release()
        cv2.destroyAllWindows()
        cap = None
        # Convert frame to ImageTk.PhotoImage object
        imgBlank = np.zeros((480,640), np.int8)
        img = Image.fromarray(imgBlank)
        img_tk = ImageTk.PhotoImage(image=img)
        # Update label with new frame
        label.config(image=img_tk)
        label.image = img_tk
        


# Function to update the camera frame in the GUI
def update_frame():
    global hand_volume_control, scaleValue
    if cap is not None:
        ret, frame = cap.read()
        if ret:
            if detectHand is not False:
                frame, vol = hand_volume_control.run(frame)
                scaleValue.set(vol)
                
            # Convert frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Resize frame to fit in GUI window
            frame_rgb = cv2.resize(frame_rgb, (640, 480))
            # Convert frame to ImageTk.PhotoImage object
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(image=img)
            # Update label with new frame
            label.config(image=img_tk)
            label.image = img_tk
            
    # Schedule next frame update after 5 ms
    label.after(5, update_frame)


# Create a frame to hold the camera frame label
frame = ttk.Frame(root)
frame.pack(pady=10)

# Create a label to display the camera frame
label = ttk.Label(frame)
label.pack()

# Create "Open Camera" button
open_button = ttk.Button(root, text="Open Camera", command=open_camera)
open_button.pack(pady=5)

# Create "Close Camera" button
close_button = ttk.Button(root, text="Close Camera", command=close_camera)
close_button.pack(pady=5)

# Create " Hand detection " toggle button
hd_toggle_button = ttk.Button(root, text="ON",image=hndOn, command= detectToggle)
hd_toggle_button.pack(pady=5)

#slider that shows the current volume by changing hand gestures.
scaleValue = tk.IntVar()
slider = ttk.Scale(
    root,
    from_=0,
    to=100,
    orient='horizontal',
    variable= scaleValue
)


# Apply some styling to the buttons
style = ttk.Style()
style.configure("TButton", padding=10, font=("Helvetica", 12))


# Start updating frames
update_frame()

# Run the GUI event loop
root.mainloop()


