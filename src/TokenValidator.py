import os
import json
import requests
import pyppeteer
import asyncio

with open(os.path.join(os.getcwd(), "data", "VARS.json"), "r") as f: VARS = json.load(f)
for var in VARS.keys():
    if VARS[var] == "":
        raise Exception(f"Must set string value for data variable {var} in data/VARS.json")

BASE_URL = "api.spotify.com"
USER_AGENT = VARS["USER_AGENT"]
FILE_PATH = os.path.join(os.getcwd(), "data", "OAuth.json")

class TokenValidator():    
    def __init__(self):
        with open(FILE_PATH, "r") as f:
            self.cache = json.load(f)
        
        self.accessToken = self.cache["accessToken"] if "accessToken" in self.cache else None
        self.refreshToken = self.cache["refreshToken"] if "refreshToken" in self.cache else None
        self.accessTokenExpiration = None
        self.isAlive = False
        self.isAuthorized = True

    def sendRequest(self, apiCall):
        headers = {
            "Accept": "*/*",
            "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {self.accessToken}",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"

        }
        response = requests.get(("https://"+BASE_URL+apiCall), headers=headers)
        if response.status_code != 401:
            self.isAlive = True
            return True
        else:
            print("Error: \n" + response.content.decode("UTF-8"))
            return False
    def sendRequestOther(self, apiCall):
        headers = {
            "Accept": "*/*",
            "User-Agent": USER_AGENT,
            "Authorization": f"Bearer {self.accessToken}",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"

        }

        response = requests.get(("https://"+"guc3-spclient.spotify.com"+apiCall), headers=headers)

        if response.status_code != 401:
            self.isAlive = True
            return True
        else:
            print("Error: \n" + response.content.decode("UTF-8"))
            return False

    def checkTokenValidity(self):
        return self.sendRequest("/v1/me")

    def refreshAccessToken(self):
        headers = {
            "Accept": "*/*",
            "cookie": f"sp_dc={self.refreshToken}",
            "User-Agent": USER_AGENT,
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site"
        }

        response = requests.get("https://open.spotify.com/get_access_token?reason=transport", headers=headers)
        content = response.json()

        if content["accessToken"] == "None":
            self.isAuthorized = False
            print("FAILED")
            print(content)
        else:
            self.accessToken = content["accessToken"]
            self.updateOAuth()
            
    def updateOAuth(self):
        cache = {"accessToken": self.accessToken, "refreshToken": self.refreshToken}
        with open(FILE_PATH, "w") as f:
            json.dump(cache, f)
    
    async def __generate(self):
        self.refreshAccessToken()
        if not self.isAuthorized:
            print("Refresh token has expired or was not retrieved.")
            browser = await pyppeteer.launch(defaultViewport={"width": VARS["SCREEN_WIDTH"], "height": VARS["SCREEN_HEIGHT"]}, ignoreDefaultArgs=['--mute-audio'])
            print("Logging on to Spotify.")
            page = await browser.newPage()
            
            await page.setUserAgent(VARS["USER_AGENT"])
            await page.goto("https://accounts.spotify.com/en/login?continue=https:%2F%2Fopen.spotify.com%2F")
            await page.type("#login-username", VARS["SPOTIFY_USER"])
            await page.type("#login-password", VARS["SPOTIFY_PWD"])
            await page.click("#login-button")
            await page.waitForNavigation()
            
            token_info = await page.evaluate("() => {const token_script = document.getElementById( 'config' );const token_json = token_script.text.trim();const token_info = JSON.parse( token_json );return token_info;}")
            cookies = await page.cookies()
            
            for cookie in cookies:
                if cookie["name"] == "sp_dc":
                    self.refreshToken = cookie["value"]
            
            await browser.close()
            
            self.accessToken = token_info["accessToken"]
            self.clientId = token_info["clientId"]
            self.accessTokenExpiration = token_info["accessTokenExpirationTimestampMs"]

            self.updateOAuth()
    def generate(self):
        asyncio.get_event_loop().run_until_complete(self.__generate())
    def refresh(self):
        if self.checkTokenValidity() == False:
            self.generate()   