import json
import time
import requests



class Player():
    def __init__(self, name):
        self.SERVER_URL = "https://api.artifactsmmo.com"
        self.API_TOKEN = self.get_api_token()
        self.name = name


    def get_api_token(self):
        with open("secret.txt") as file:
            token = file.readlines()[0]
        return token


    def move(self, x, y):
        url, headers = self.get_post_request("move")
        json_body = {"x": x, "y": y}

        response = requests.post(url, headers=headers, json=json_body)
        data = response.json()
        self.cooldown_timer(data)


    def fight(self):
        url, headers = self.get_post_request("fight")
        response = requests.post(url, headers=headers)
        data = response.json()

        self.cooldown_timer(data)


    def fight_looping(self):
        while True:
            self.fight()
            self.rest()


    def rest(self):
        url, headers = self.get_post_request("rest")
        response = requests.post(url, headers=headers)
        data = response.json()
        self.cooldown_timer(data)


    def cooldown_timer(self, data):
        cooldown = data["data"]["cooldown"]["total_seconds"]
        print(f"Sleeping for {cooldown} seconds")
        time.sleep(cooldown)


    def get_post_request(self, action):
        url = f"{self.SERVER_URL}/my/{self.name}/action/{action}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.API_TOKEN}"
        }
        return url, headers


if __name__ == '__main__':
    BlueMaiden = Player("BlueMaiden")
    BlueMaiden.fight()
    # move("BlueMaiden", 0, 1)
    # fight("BlueMaiden")
    # rest("BlueMaiden")


























