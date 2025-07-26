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
        self.ws_mining_coords = (1, 5)

    def get_api_token(self):
        with open("secret.txt") as file:
            token = file.readlines()[0]
        return token

    def get_post_request(self, action):
        """
        Return appropriate POST request URLs based in action suffix
        :param action:
        """
        url = f"{self.SERVER_URL}/my/{self.name}/action/{action}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.API_TOKEN}"
        }
        return url, headers

    def get_get_request(self, action):
        """
        Return appropriate GET request URLs based in action suffix
        :param action:
        """
        url = f"{self.SERVER_URL}/my/{action}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.API_TOKEN}"
        }
        return url, headers

    def get_character_data(self):
        """
        Get all characters' metadata as JSON.
        Needed for depositing.
        """
        url, headers = self.get_get_request("characters")

        response = requests.get(url, headers=headers)
        data = response.json()
        return data

    def check_banking(self, response):
        """
        If response code 497, player has a full inventory and needs to deposit.
        :param response:
        """
        if response.status_code == 497:
            self.move(*self.bank_coords)
            self.deposit()
            self.move(*self.coords)

    def check_loss(self, data):
        """
        Receive json data of a response.
        If a fight is lost, heal and return to the coordinates.
        """
        try:
            if data["data"]["fight"]["result"] == "loss":
                self.rest()
                self.move(*self.coords)
        except KeyError:
            print(f"[{self.name}]: Could not find data, likely a start-up error")

    def get_inventory_list(self):
        """
        Get inventory of current character and return as JSON.
        Needed to deposit items into bank.
        """
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

    def withdraw(self, item, amount):
        """
        Withdraw an item with given amount of the bank.
        Must use the correct item name!
        :param item:
        :param amount:
        """
        url, headers = self.get_post_request("bank/withdraw/item")
        json_body = json.dumps([{ "code": item, "quantity": amount }])

        response = requests.post(url, headers=headers, data=json_body)
        if response.status_code <= 200:
            data = response.json()
            print(f"[{self.name}]: Withdrawing {amount}x {item}")
            self.cooldown_timer(data)
            return True
        else:
            print(f"[{self.name}]: No more {item} in bank!")
            return False

    def deposit(self):
        """
        Check current inventory of character and deposit everything into bank

        @requires: Must be standing on bank place
        """
        inventory = self.get_inventory_list()
        url, headers = self.get_post_request("bank/deposit/item")

        response = requests.post(url, headers=headers, data=inventory)
        data = response.json()
        print(f"[{self.name}]: Dumping inventory")
        self.cooldown_timer(data)

    def craft(self, item, amount):
        """
        Craft an item for a specified amount.
        Must be standing on any crafting place. Must be using correct item codes.
        """
        url, headers = self.get_post_request("crafting")
        json_body = json.dumps({ "code": item, "quantity": amount })

        response = requests.post(url, headers=headers, data=json_body)
        if response.status_code <= 200:
            data = response.json()
            print(f"[{self.name}]: Crafting {amount}x {item}")
            self.cooldown_timer(data)
            return True
        else:
            print(f"[{self.name}]: Cannot craft! Bad state!")
            return False

    def move(self, x, y):
        """
        Move to coordinates
        :param x:
        :param y:
        """
        url, headers = self.get_post_request("move")
        json_body = {"x": x, "y": y}

        response = requests.post(url, headers=headers, json=json_body)
        data = response.json()
        self.cooldown_timer(data)

    def fight(self):
        """
        Fight at current place.
        Checks for full inventory and if fight is lost
        """
        url, headers = self.get_post_request("fight")
        response = requests.post(url, headers=headers)
        data = response.json()

        self.cooldown_timer(data)
        self.check_banking(response)
        self.check_loss(data)

    def fight_loop(self):
        """
        Keep fighting indefinitely at current place.
        Always switch between fight and rest.
        """
        self.move(*self.coords)
        while True:
            self.fight()
            self.rest()

    def rest(self):
        """
        Regain all HP
        """
        url, headers = self.get_post_request("rest")
        response = requests.post(url, headers=headers)
        data = response.json()
        self.cooldown_timer(data)

    def cooldown_timer(self, data):
        """
        Receive JSON response data and wait for its cooldown
        :param data of requests.response:
        """
        try:
            cooldown = data["data"]["cooldown"]["total_seconds"]
        except KeyError:
            print(f"[{self.name}] [{data['error']['code']}]: {data['error']['message']}")
            return

        time.sleep(cooldown)

    def gather(self):
        """
        Gather resources at current place
        """
        url, headers = self.get_post_request("gathering")
        response = requests.post(url, headers=headers)
        data = response.json()
        self.cooldown_timer(data)
        self.check_banking(response)

    def gather_loop(self):
        """
        Gather resources at current place indefinitely
        """
        self.move(*self.coords)
        while True:
            self.gather()

    def craft_copper_bars(self):
        """
        Craft copper bars in the Mining Workshop (1, 5)
        Stop when withdrawing copper ore from bank doesnt work
        """
        while True:
            self.move(*self.bank_coords)
            # if the withdraw fails, theres no more copper and we can stop
            if not self.withdraw("copper_ore", 80):
                break
            self.move(*self.ws_mining_coords)
            self.craft("copper_bar", 8)



if __name__ == '__main__':
    pass
    BlueMaiden = Player("BlueMaiden")
    BlueMaiden.craft_copper_bars()
    # move("BlueMaiden", 0, 1)
    # fight("BlueMaiden")
    # rest("BlueMaiden")
