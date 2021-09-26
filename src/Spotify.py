import json
import os
import requests

with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "VARS.json"), "r") as f: VARS = json.load(f)
for var in VARS.keys():
    if VARS[var] == "":
        raise Exception(f"Must set string value for data variable {var} in data/VARS.json")

class Spotify():
    def __init__(self, validator):
        self.USER_AGENT = VARS["USER_AGENT"]
        self.BASE_URL = "https://api.spotify.com"
        self.validator = validator
    def __sendRequest(self, apiCall, type="GET"):
        headers = {
            "Accept": "*/*",
            "User-Agent": self.USER_AGENT,
            "Authorization": f"Bearer {self.validator.accessToken}",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"
        }
        response = None
        if type == "GET":
            response = requests.get((self.BASE_URL+apiCall), headers=headers)
        elif type == "PUT":
            response = requests.put((self.BASE_URL+apiCall), headers=headers)
        elif type == "POST":
            response = requests.post((self.BASE_URL+apiCall), headers=headers)
        else:
            raise Exception(f"Unsupported request type: {type}")
        
        content = json.loads(response.content.decode("UTF-8")  or "{}")
        if response.status_code in [400,401,403,404,429,500,502,503]:
            print(f"{response.status_code} Error:")
            print(content)
            if content["error"]["message"] == "The access token expired":
                print("The access token expired.")
                print(".....................................\nNow generating new access code\n")
                self.validator.refresh()
                print("Done. Retrying request.")
                return self.__sendRequest(apiCall, type)
            else:
                raise Exception(f"\n{response.status_code} Error:\n{content}")
        elif response.status_code == 200:
            return content
        elif response.status_code == 204:
            return True
        else:
            raise Exception(f"Unknown error {response.status_code}:\nResponse:\n{response}")
            
    def isPlaying(self):
        res = self.__sendRequest("/v1/me/player/", "GET")
        if res["is_playing"] == True:
            return True
        else:
            return False
    def getDevices(self):
        res = self.__sendRequest("v1/me/player/devices", "GET")
        return res["devices"]

    def getVolume(self):
        res = self.__sendRequest("/v1/me/player/", "GET")
        return res["device"]["volume_percent"]

    def getPlaylist(self, playListId):
        res = self.__sendRequest(f"/v1/playlists/{playListId}/tracks", "GET")
        return res

    def setVolume(self, percent):
        res = self.__sendRequest(f"/v1/me/player/volume?volume_percent={percent}", "PUT")
        return res

    def playPause(self):
        res = self.__sendRequest(f"/v1/me/player/{'play' if self.isPlaying() == False else 'pause'}", "PUT")
        return res

    def playNext(self):
        res = self.__sendRequest(f"/v1/me/player/next/", "POST")
        return res

    def playPrevious(self):
        res = self.__sendRequest(f"/v1/me/player/previous/", "POST")
        return res


