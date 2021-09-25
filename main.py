import cv2  
import time
from src.HandTracking import *
from src.Spotify import *
from src.TokenValidator import *


def volume(upCount, fingersUp, spotify):
    if upCount == 4 and fingersUp[1] == 0:
        volume = spotify.getVolume()+10
        print("Increasing volume to:")
        print(volume)
        spotify.setVolume(volume if volume <= 100 else 100)
        return True
    elif upCount == 4 and fingersUp[3] == 0:
        volume = spotify.getVolume()-10
        print("Decreasing volume to:")
        print(volume)
        spotify.setVolume(volume if volume >= 0 else 0)
        return True
    return False

def playNext(upCount, fingersUp, spotify):
    if upCount == 2 and fingersUp[1] == 1 and fingersUp[2] == 1:
        spotify.playNext()
        time.sleep(0.2)
        return True
    return False

def playPrevious(upCount, fingersUp, spotify):
    if upCount == 3 and fingersUp[1] == 1 and fingersUp[2] == 1 and fingersUp[3] == 1:
        spotify.playPrevious()
        time.sleep(0.2)
        return True
    return False

def playPause(upCount, fingersUp, spotify):
    if upCount == 4 and fingersUp[2] == 0:
        spotify.playPause()
        return True
    return False

def main():
    w, h = 1280, 720
    capture = cv2.VideoCapture(0)
    capture.set(3, w)
    capture.set(4, h)

    detector = HandDetector(max_num_hands = 2, min_detection_confidence=0.75, min_tracking_confidence=.5)
    validator = TokenValidator()
    spotify = Spotify(validator)

    area = 0

    while True:
        success, img = capture.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img, draw=False, bounding=True)
        if len(lmList) != 0:
            area = (bbox[2]-bbox[0]) * (bbox[3]-bbox[1]) // 100
            if area > 150:
                fingersUp, upCount = detector.fingersUp()
                if playPause(upCount, fingersUp, spotify): pass
                elif playNext(upCount, fingersUp, spotify): pass
                elif playPrevious(upCount, fingersUp, spotify): pass
                elif volume(upCount, fingersUp, spotify): pass
            
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    with open(os.path.join(os.getcwd(), "data", "VARS.json"), "r") as f: VARS = json.load(f)
    if VARS["SPOTIFY_USER"] == "" or VARS["SPOTIFY_PWD"] == "" or VARS["USER_AGENT"] == "" or VARS["SCREEN_WIDTH"] == "" or VARS["SCREEN_HEIGHT"] == "":
        print("Please run setup.py as program data has not been initialized")
    else:
        main()