# Spotify Gestures

Spotify Gestures is a simple program that allows you to carry out basic functions in Spotify like skipping playback, playing/pausing, and adjusting volume with simple, visual gestures.

## Requirements
- Latest version of Python installed
- Required libraries installed
    - Run the following command in this directory to install required libraries:
    ```
    pip install -r requirements.txt
    ```
## Usage
1. Run `setup.py` and set your spotify username, password, and *User Agent*
    - You can obtain your User Agent by navigating to this link in your browser and copying the User Agent: https://www.whatismyip.com/user-agent/
2. Run `main.py` and enjoy!

     ### **Gestures**
    - With all 5 fingers up, flick middle finger down to Play/Pause
    - With all 5 fingers up, flick ring finger down to lower volume
    - With all 5 fingers up, flick index finger down to increase volume
    - Hold three fingers up (Index, Middle, Ring) to skip to previous track
    - Hold two fingers up (Index, Middle) to skip to next track
3. Navigate to the camera window and press "x" to quit the program

## Note
- Initial run of `main.py` will taker longer as resources are setup for the first time
- This project works best with a clear background from which the hand only enters the frame when conducting gestures *for* Spotify Gestures *(I recommend tilting your webcam up towards the ceiling)*
- Make sure you have a spotify device active (e.g. Web Player is online or the Spotify App is running)

### *I hope you enjoy using Spotify Gestures! Feel free to report any issues (Or ask for features) or submit pull requests to improve this project*