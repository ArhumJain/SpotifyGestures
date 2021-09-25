import tkinter
import os
import json
from src.TokenValidator import *

def main():
    validator = TokenValidator()
    path = os.path.join(os.getcwd(), "data", "VARS.json")
    
    with open(path, "r+") as f:
        data = json.loads(f.read())
        PWD_VERIFIED = False
        USER = input("Spotify Username (Email): ")
        while not PWD_VERIFIED:
            PWD = input("Spotify Password: ")
            PWD_CONFIRM = input("Confirm Password: ")
            if PWD != PWD_CONFIRM:
                print("Passwords do not match, try again")
            else:
                PWD_VERIFIED = True
        
        USER_AGENT = input("Browser User Agent: ")

        root = tkinter.Tk()

        SCREEN_WIDTH = root.winfo_screenwidth()
        SCREEN_HEIGHT = root.winfo_screenheight()

        data["SPOTIFY_USER"] = USER
        data["SPOTIFY_PWD"] = PWD
        data["USER_AGENT"] = USER_AGENT
        data["SCREEN_WIDTH"] = SCREEN_WIDTH
        data["SCREEN_HEIGHT"] = SCREEN_HEIGHT
        
        validator.refresh()

        print(".................")
        print("Set up complete. You can now run main.py to run the program.") 
    with open(path, "w") as f:
        json.dump(data, f)

        
if __name__ == "__main__":
    main()