# virtualSoundControler
* Developed a Hand Gestures Volume Control System using 
Python, leveraging OpenCV for computer vision. Created an 
intuitive method to adjust audio playback volume using hand 
gestures captured by a camera. 
* Achieved benchmarks of 90-95% accuracy in gesture 
recognition.
* The system utilizes a camera to capture and interpret user 
hand gestures, providing a natural way to control volume levels.

## To Execute the project 

Step 1: install python 3.10 just because the Deep Learning module mediaPipe doesn't support the latest version of Python.

Step 2: make an alias 

    $ New-Alias -Name python310 -value "yourPython3.10.exe path"


Step 3: Create a Virtual Environment 

    $ python310 -m venv venv310

Step 4: Activate the virtual environment

    $ venv310\scripts\activate

Step 5: Install the mediaPipe module

    $ py -m pip install mediapipe


Step 6: Install the project's dependencies 

    $ pip install -r requirements.txt


Step 7: To run the project 

    $ python gui.py


## Demo of the project with all its features such as volume control and hand tracking feature

https://github.com/kunal9922/virtualSoundControler/assets/53283003/967d553c-333c-47e5-9452-0458bc314606


## Started with Hand Tracking

https://github.com/kunal9922/virtualSoundControler/assets/53283003/1d18bca4-6291-4fe0-84cb-5beda68c91a9


## Hand Landmarks 
<img src = ".\dataset\hand_landmarks.png">
