import cv2
import tkinter as tk
from PIL import Image, ImageTk

# OpenCV VideoCapture object for camera input
cap = cv2.VideoCapture(0)

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

# Function to update the camera frame in the GUI
def update_frame():
    if cap is not None:
        ret, frame = cap.read()
        if ret:
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
    # Schedule next frame update after 10 ms
    label.after(10, update_frame)

# Create the main window
root = tk.Tk()
root.title("Camera Viewer")

# Create a label to display the camera frame
label = tk.Label(root)
label.pack()

# Create "Open Camera" button
open_button = tk.Button(root, text="Open Camera", command=open_camera)
open_button.pack()

# Create "Close Camera" button
close_button = tk.Button(root, text="Close Camera", command=close_camera)
close_button.pack()

# Start updating frames
update_frame()

# Run the GUI event loop
root.mainloop()

# Release the VideoCapture object and close all OpenCV windows
if cap is not None:
    cap.release()
cv2.destroyAllWindows()
