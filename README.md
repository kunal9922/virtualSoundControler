# virtualSoundControler
It is my college project where we are building a python software that can control volume by using Hand Gesture in Real Time 

To initiate the project 
step 1: 
    * install python 3.10 just becoz mediapipe module doesn't support latest version of python for now.

step2:
   * make alias 

     New-Alias -Name python310 -value "yourPython3.10.exe path"

     

step 3: 

create virtual env 

python310 -m venv venv310

step 4:

Activate virtual environment

venv310\scripts\activate

Step 5: install mediapipe module

py -m pip install mediapipe


Step 6 install dependencies 
pip install -r requirements.txt


step 7 to run project 

python gui.py

# Sample pics 

<img src = "./dataset/demopic.png">

<h1>Demo Of Hand Tracking</h1>

<video width="360" height="240" controls>  <source src="./dataSet/demoHandTracking1.mp4" type="video/mp4">  </video>

<img src = "./dataset/demo_hand_sound_Control.gif">



