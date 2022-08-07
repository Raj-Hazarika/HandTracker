# HandTracker
This is a simple hand tracking application for mac users. This application performs various tasks such as volume control, brightness change, opening browser etc., based on the hand gestures by the user.

# How to use?

- Download all the files.
- Make sure all the modules used are installed. This program uses mediapipe, cv2, numpy and subprocess, which are required to be downloaded.
- This program is meant for mac users. Although, the system commands can be updated for windows and linux users as well.
- The given code is written in python 3.0 and requires a web cam.


### HandTrackingModule.py

- This module is responsible to track down the hand gestures and movement of the user. The module mediapipe is used to track these movements and cv2 is used to access the webcam and process the video.
- Each joint in the hand is assigned a numerical value which is used to access its location in the footage.


### MainProject.py

- This script performs various tasks based on the user's hand gestures. 
- The tasks that can be performed are volume change, brightness change and opening various tabs in the browser.
- These tasks can also be changed based on the user's perference by simply tweaking the script. Even, more task can be added for different hand gestures which are not being used.

### Tasks and the hand gestures

1. If the thumb of right and left hand are touched together then the brightness increases. However, if the pinky of right and left hand are touched then brightness decreases.
2. 
3. 
