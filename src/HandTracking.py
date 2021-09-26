import math
import cv2
import mediapipe as mp
import time

from mediapipe.framework.formats.landmark_pb2 import LandmarkList

class HandDetector():
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.mediapipe.python.solutions.hands
        self.hands = self.mpHands.Hands(self.static_image_mode, self.max_num_hands, self.min_detection_confidence, self.min_tracking_confidence) # Adjust parameters to adjust confidence detection/tracking
        self.mpDraw = mp.solutions.mediapipe.python.solutions.drawing_utils

        self.tipIds = [4,8,12,16,20]

    def findHands(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for lms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, lms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True, bounding=False):
        try: self.results
        except: raise Exception("Call HandDetector object function, findHands, before calling HandDetector object function, findPosition")
        
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in  enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                xList.append(cx)
                yList.append(cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255,0,0), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin,ymin,xmax,ymax
            if bounding:
                cv2.rectangle(img, (bbox[0]-20, bbox[1]-20), (bbox[2]+20, bbox[3]+20), (0,255,0), 2)
        return self.lmList, bbox

    def getHand(self):
        print(self.results.multi_handedness)
    def fingersUp(self):
        try: self.lmList
        except: raise Exception("Call HandDetector object function, findPosition, before calling HandDetector object function, findDistance")
        
        fingers = []
        upCount = 0
        
        if self.lmList[self.tipIds[0]][1] > self.lmList[5][1]: 
            fingers.append(1)
            upCount += 1
        else: 
            fingers.append(0)
        for i in range(1,5):
            if self.lmList[self.tipIds[i]][2] < self.lmList[self.tipIds[i] - 2][2]: 
                fingers.append(1)
                upCount += 1
            else: 
                fingers.append(0)

        return fingers, upCount

    def landmarkBelow(self, lm1, lm2):
        try: 
            self.lmList
            try:
                self.lmList[lm1] or self.lmList[2]
            except:
                raise Exception("One or both of the landmarks do not exist")
        except: 
            raise Exception("Call HandDetector object function, findPosition, before calling HandDetector object function, findDistance")
        
        if self.lmList[lm1][2] <= self.lmList[lm2][2]:
            return True
        else:
            return False
        
    def findDistance(self, p1, p2, img, draw=True):
        try: self.lmList
        except: raise Exception("Call HandDetector object function, findPosition, before calling HandDetector object function, findDistance")
        
        x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
        x2, y2 = self.lmList[p2][1], self.lmList[p2][2]

        if draw:
            cv2.line(img, (x1, y1), (x2,y2), (0,255,0), 4)
            cv2.circle(img, (x1,y1), 20, (255,0,0), cv2.FILLED)
            cv2.circle(img, (x2,y2), 20, (255,0,0), cv2.FILLED)
            cv2.circle(img, (75,90),45, (0,255,0), cv2.FILLED)

        distance = math.hypot(y1-y2, x1-x2)
        return distance, img, [x1,y1,x2,y2]

    def findAngle(self, lm1, lm2, lm3, draw=True):
        try: self.lmList
        except: raise Exception("Call HandDetector object function, findPosition, before calling HandDetector object function, findDistance")
        
        a = (self.lmList[lm1][1], self.lmList[lm1][2])
        b = (self.lmList[lm2][1], self.lmList[lm2][2])
        c = (self.lmList[lm3][1], self.lmList[lm3][2])
        angle = abs(math.degrees(math.atan2(a[1]-b[1], a[0]-b[0]) - math.atan2(c[1]-b[1], c[0]-b[0])))
        angle = 360-angle if angle > 180 else angle
        return angle

def main():
    pTime = 0
    cTime = 0    
    capture = cv2.VideoCapture(0)
    detector = HandDetector(min_detection_confidence=.75)
    
    while True:
        success, img = capture.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255))
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()
