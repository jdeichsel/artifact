import json
import time
import requests


class Player:
    def __init__(self, name):
        self.SERVER_URL = "https://api.artifactsmmo.com"
        self.API_TOKEN = self.get_api_token()
        self.name = name
        self.coords = (None, None)
        self.bank_coords = (4, 1)

    def get_api_token(self):
        with open("secret.txt") as file:
            token = file.readlines()[0]
        return token


    def get_post_request(self, action):
        url = f"{self.SERVER_URL}/my/{self.name}/action/{action}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.API_TOKEN}"
        }
        return url, headers


    def get_get_request(self, action):
        url = f"{self.SERVER_URL}/my/{action}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.API_TOKEN}"
        }
        return url, headers


    def get_character_data(self):
        url, headers = self.get_get_request("characters")

        response = requests.get(url, headers=headers)
        data = response.json()
        return data


    def check_banking(self, response):
        if response.status_code == 497:
            self.move(*self.bank_coords)
            self.deposit()
            self.move(*self.coords)


    def get_inventory_list(self):
        character_data = self.get_character_data()

        for character in character_data.get("data", []):
            if character.get("name") == self.name:
                inventory = character.get("inventory", [])
                break

        if inventory:
            filtered_inventory = [item for item in inventory if item.get('code') != ""]

            for item in filtered_inventory:
                item.pop('slot', None)

            inventory = json.dumps(filtered_inventory)
            return inventory
        return None


    def deposit(self):
        inventory = self.get_inventory_list()
        url, headers = self.get_post_request("bank/deposit/item")

        response = requests.post(url, headers=headers, data=inventory)
        data = response.json()
        print(f"[{self.name}]: Dumping inventory")
        self.cooldown_timer(data)


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
        self.check_banking(response)


    def fight_loop(self):
        self.move(*self.coords)
        while True:
            self.fight()
            self.rest()


    def rest(self):
        url, headers = self.get_post_request("rest")
        response = requests.post(url, headers=headers)
        data = response.json()
        self.cooldown_timer(data)


    def cooldown_timer(self, data):
        try:
            cooldown = data["data"]["cooldown"]["total_seconds"]
        except KeyError:
            print(f"[{self.name}] [{data['error']['code']}]: {data['error']['message']}")
            return

        time.sleep(cooldown)


    def gather(self):
        url, headers = self.get_post_request("gathering")
        response = requests.post(url, headers=headers)
        data = response.json()
        self.cooldown_timer(data)
        self.check_banking(response)


    def gather_loop(self):
        self.move(*self.coords)
        while True:
            self.gather()





if __name__ == '__main__':
    pass
    # MiningMaiden = Player("MiningMaiden")
    # MiningMaiden.coords = (2, 0)
    # MiningMaiden.check_banking()
    # BlueMaiden = Player("BlueMaiden")
    # BlueMaiden.fight()
    # move("BlueMaiden", 0, 1)
    # fight("BlueMaiden")
    # rest("BlueMaiden")


























