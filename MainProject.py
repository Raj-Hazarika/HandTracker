import math
import cv2
import time
import numpy as np
import HandTrackingModule as htm
from subprocess import call
import os

wCam, hCam = 640, 480
pTime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.HandDetector(detectionCon=0.7)
two_hands = False
rickRolling = True
main_loop = True
browser = [True, True, True]
r_hand = []
l_hand = []


def find_length(point1, point2, lm1, lm2):
    """
    Finds the distance between two points (the points refers to landmarks in the hands)
    :param point1: an integer referring to the first point
    :param point2: an integer referring to the second point
    :param lm1: list containing positional info for the first hand
    :param lm2: list containing positional info for the first hand
    :return: length between the two points
    """
    point1_x, point1_y = lm1[point1][1], lm1[point1][2]
    point2_x, point2_y = lm2[point2][1], lm2[point2][2]

    length = math.hypot(point1_x - point2_x, point1_y - point2_y)
    return length


def rick_roll(rick):
    """
    Opens a youtube link to rick roll the user.
    :param rick: a boolean, if True, rick roll else don't
    :return: False
    """
    hypo = find_length(4, 8, lmList1, lmList1)
    perpendicular = find_length(8, 2, lmList1, lmList1)
    base = find_length(4, 2, lmList1, lmList1)
    expected_hypo = math.sqrt((perpendicular ** 2) + (base ** 2))
    if (hypo - 10) < expected_hypo < (hypo + 10):
        if rick:
            os.system("open \"\" https://www.youtube.com/watch?v=V-_O7nl0Ii0")
            return False


def change_volume(hand):
    """
    This function changes the volume of the mac device.
    The terminal script can be changed so that this works on linux or windows.
    :param hand: Right hand positional info
    :return: None
    """
    length = find_length(4, 8, lmList1, lmList1)
    if length < 110 and hand[2]:  # to change the volume, the middle finger and thumb of the right hand is used
        volume = (np.interp(length, [10, 110], [0, 100])//10) * 10
        volumeLine = 'set volume output volume ' + str(volume)
        call(["osascript -e " + "'" + volumeLine + "'"], shell=True)


def change_brightness():
    """
    Increases or decreases the brightness of the mac device as per the user's instructions.
    The terminal script can be changed so that this works on linux or windows.
    :return: None
    """
    if two_hands:
        tap_thumb = find_length(4, 4, lmList1, lmList2)
        if tap_thumb < 30:  # if the thumbs of bith the hands touch each other, brightness is increased.
            call(["""osascript -e 'tell application "System Events"' -e 'key code 144' -e ' end tell'"""],
                 shell=True)
        tap_pinky = find_length(20, 20, lmList1, lmList2)
        if tap_pinky < 30:  # if the thumbs of bith the hands touch each other, brightness is decreased.
            call(["""osascript -e 'tell application "System Events"' -e 'key code 145' -e ' end tell'"""],
                 shell=True)


def finger_count(lm):
    """
    This function returns a list for a given hand. The list elements are 0 or 1 depending upon whether the finger is up or not.
    :param lm: list for the given hand
    :return: finger positions
    """
    tipIds = [4, 8, 12, 16, 20]
    fingers = []
    if len(lm) != 0:
        if lm[tipIds[0]][1] > lm[tipIds[0] - 1][1]:  # if finger is up then 1 is appended
            fingers.append(1)
        else:
            fingers.append(0)  # else if the finger is down then 0 is appended

        for id in range(1, 5):
            if lm[tipIds[id]][2] < lm[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
    return fingers


while main_loop:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList1, bbox1 = detector.findPosition(img, 0)
    r_hand = finger_count(lmList1)
    try:
        lmList2, bbox2 = detector.findPosition(img, 1)
        two_hands = True
    except:
        two_hands = False
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    if len(lmList1) != 0:

        area1 = ((bbox1[2] - bbox1[0])*(bbox1[3] - bbox1[1]))//100
        if 250 < area1 < 1000:
            # Changing volume
            change_volume(r_hand)

            # Changing brightness
            change_brightness()

            # RickRoll
            rickRolling = rick_roll(rickRolling)

            # Finger Count
            # Restarts browser open count
            if r_hand == [1, 0, 0, 0, 1]:  # if pinky and thumb are up then rick roll
                rickRolling = True
                for i in range(len(browser)):
                    browser[i] = True
            # Closes the program
            if r_hand == [0, 1, 1, 0, 1]:  # if index finger, middle finger and pinky is up then close the program
                main_loop = False
            # open google
            if r_hand == [0, 1, 0, 0, 0] and browser[0]:  # if only index finger is up, open google
                os.system("open \"\" https://www.google.com")
                browser[0] = False
            # open youtube
            if r_hand == [0, 1, 1, 0, 0] and browser[1]:  # if index finger and middle finger is up, open youtube
                os.system("open \"\" https://www.youtube.com")
                browser[1] = False
            # open github
            if r_hand == [0, 1, 1, 1, 0] and browser[2]:  # if index finger, middle finger and ring is up, open github
                os.system("open \"\" https://github.com/")
                browser[2] = False

    cv2.putText(img, "FPS: " + str(int(fps)), (40, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

    cv2.imshow("Img", img)
    cv2.waitKey(1)
