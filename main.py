import cv2  
import numpy as np
import src.HandTracking as ht
from src.Spotify import *
from src.TokenValidator import *
w, h = 1280, 720
capture = cv2.VideoCapture(0)
capture.set(3, w)
capture.set(4, h)

detector = ht.HandDetector(max_num_hands = 2, min_detection_confidence=0.75, min_tracking_confidence=.5)
validator = TokenValidator()
spotify = Spotify(validator)

vol = 0
volBar = 400
volPer = 0
area = 0

fingersFive = False
def volume(img):
    area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1]) // 100        
    if area > 150:
        if upCount == 5 or (upCount == 4 and fingersUp[3] == 0):
            distance, img, lineInfo = detector.findDistance(4, 8, img, draw=False)

            minDist = 35
            maxDist = 180
            volBar = np.interp(distance, [minDist, maxDist], [400,150])
            volPer = np.interp(distance, [minDist,maxDist], [0,100])

            increment = 10
            volPer = increment * round(volPer/increment)
            
            
            if not detector.landmarkBelow(16, 11) and upCount == 4: 
                print(f"Setting volume to: {volPer/100}")
                # spotify.setVolume(volPer)    
            if distance <= 30:
                cv2.circle(img, (75,90), 45, (0,0,255), cv2.FILLED)
            
            cv2.rectangle(img, (50, 150), (85, 400), (255,0,0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255,0,0), cv2.FILLED)
            cv2.putText(img, f"{int(volPer)}%", (60,455), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 3)

def playNext(img):
    if upCount == 2:
        pass

def playPause():
    if upCount == 2 and fingersUp[0] == 1 and fingersUp[1] == 1:
        if detector.findAngle(4,0,8) < 8:
            spotify.playPause()
            
while True:
    success, img = capture.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False, bounding=True)
    if len(lmList) != 0:
        fingersUp, upCount = detector.fingersUp()
        playPause()

    cv2.imshow("Image", img)
    cv2.waitKey(1)