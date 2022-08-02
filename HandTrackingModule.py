import cv2
import mediapipe as mp
import time


class HandDetector:
    def __init__(self, mode=False, maxHands=2, model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity = model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.model_complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        """
        Detects the hands of the user in the provided footage.
        :param img: the footage recorded by the web cam of the device
        :param draw: if True, the connecting points on the hands are shown in the footage
        :return: img
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0):
        """
        Finds the position of the hand in the footage.
        :param img: the footage recorded by the web cam of the device
        :param handNo: if 0, only the first hand recorded in the footage is processed. If 2, both the hands are processed.
        :return: lmlist, bbox
        """
        xList = []
        yList = []
        lmlist = []  # initializing a nested list whose elements are list containing info about hand position
        bbox = []  # another list containing info about an imaginary boundary box made along the boundary of the hand.
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                xList.append(cx)
                yList.append(cy)

            xmax, xmin = max(xList), min(xList)
            ymax, ymin = max(yList), min(yList)

            bbox = [xmin, ymin, xmax, ymax]
            print(lmlist, bbox)
        return lmlist, bbox


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)  # capturing footage using the webcam of the given device. If main webcam not being used, try using 1 instead of 0
    detector = HandDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    main()