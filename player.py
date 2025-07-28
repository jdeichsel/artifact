import json
import time
import requests
from colorama import init, Fore, Style
from datetime import datetime


class Player:
    def __init__(self, name):
        init()  # for colored cmd prints
        self.SERVER_URL = "https://api.artifactsmmo.com"
        self.API_TOKEN = self.get_api_token()
        self.name = name
        self.role = None
        self.coords = (None, None)

        # Workshop Coordinates
        self.bank_coords = (4, 1)
        self.ws_mining_coords = (1, 5)
        self.ws_woodcutting_coords = (-2, -3)
        self.ws_cooking_coords = (1, 1)
        self.ws_alchemy_coords = (2, 3)
        self.ws_weaponcrafting_coords = (2, 1)
        self.ws_gearcrafting_coords = (3, 1)

        # Skill levels
        self.combat = None
        self.mining = None
        self.woodcutting = None
        self.fishing = None
        self.weaponcrafting = None
        self.gearcrafting = None
        self.jewelrycrafting = None
        self.cooking = None
        self.alchemy = None

    @staticmethod
    def time():
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def color_text(text, color):
        """
        Returns a string wrapped for a specific color
        Possible colors: ``red``, ``green``, ``yellow``, ``blue``, ``magenta``,``cyan``
        :param text: input text
        :return: same text wrapped around with color operators
        """

        if color == "red":
            return Fore.RED + text + Style.RESET_ALL
        elif color == "green":
            return Fore.GREEN + text + Style.RESET_ALL
        elif color == "yellow":
            return Fore.YELLOW + text + Style.RESET_ALL
        elif color == "blue":
            return Fore.BLUE + text + Style.RESET_ALL
        elif color == "magenta":
            return Fore.MAGENTA + text + Style.RESET_ALL
        elif color == "cyan":
            return Fore.CYAN + text + Style.RESET_ALL
        else:
            print(Fore.RED + f"Invalid color: {color}" + Style.RESET_ALL)
            return text


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
        Check after depositing if theres any craftable items in bank
        """
        if response.status_code == 497:
            self.move(*self.bank_coords)
            self.deposit()

            if self.role == "mining":
                self.craft_all_bars()
            elif self.role == "wood":
                self.craft_all_planks()
            elif self.role == "fishing":
                self.craft_all_food()
            elif self.role == "alchemy":
                self.craft_all_potions()
            elif self.role == "fight":
                self.craft_all_gear()

            self.move(*self.coords)

    def check_loss(self, data):
        """
        Receive json data of a response.
        If a fight is lost, return to the coordinates.
        """
        try:
            if data["data"]["fight"]["result"] == "loss":
                self.move(*self.coords)
        except KeyError:
            print(f"[{self.name}][{self.time()}]: " + self.color_text("Could not find data, likely a start-up error", "red"))

    def get_inventory_list(self):
        """
        Get inventory of current character and return as JSON.
        Needed to deposit items into bank.
        """
        character_data = self.get_character_data()

        inventory = None
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
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Withdrawing {amount}x {item}", "cyan"))
            self.cooldown_timer(data)
            return True
        else:
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Failed to withdraw {amount}x {item}", "red"))
            return False

    def deposit(self):
        """
        Check current inventory of character and deposit everything into bank
        Depending on character role: crafts gathered materials
        @requires: Must be standing on bank place
        """
        inventory = self.get_inventory_list()
        url, headers = self.get_post_request("bank/deposit/item")

        response = requests.post(url, headers=headers, data=inventory)
        data = response.json()
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Dumping inventory", "cyan"))
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
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Crafting {amount}x {item}", "yellow"))
            self.cooldown_timer(data)
            return True
        else:
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Bad Crafting! [{response.status_code}] {response.text}", "red"))
            return False

    def recycle(self, item, amount):
        """
        You need to be standing on the workshop where you crafted the item to recycle it!
        :param item:
        :param amount:
        """
        url, headers = self.get_post_request("recycling")
        json_body = json.dumps({"code": item, "quantity": amount})

        response = requests.post(url, headers=headers, data=json_body)
        if response.status_code <= 200:
            data = response.json()
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Recycling {amount}x {item}", "yellow"))
            self.cooldown_timer(data)
        else:
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Bad Recycling! [{response.status_code}] {response.text}", "red"))

    def move(self, x, y):
        """
        Move to coordinates
        :param x:
        :param y:
        """
        url, headers = self.get_post_request("move")
        json_body = {"x": x, "y": y}


        response = requests.post(url, headers=headers, json=json_body)
        while response.status_code > 200 and response.status_code != 490:  # 490 = character already at destination
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"[{response.status_code}]: Tried moving, must be on cooldown!", "red"))
            time.sleep(5)
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
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Cooldown Timer Error! [{data['error']['code']}]: {data['error']['message']}", "red"))
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

    def craft_all_planks(self):
        """
        Cycles through all available recipes and crafts all items
        Any order is okay, no overlaps
        """
        self.craft_ash_planks()
        self.craft_spruce_planks()

    def craft_all_bars(self):
        """
        Cycles through all available recipes and crafts all items
        Any order is okay, no overlaps
        """
        self.craft_copper_bars()
        self.craft_iron_bars()

    def craft_all_food(self):
        """
        Cycles through all available recipes and crafts all items
        Any order is okay, only very small overlaps
        """
        self.craft_cooked_chicken()
        self.craft_cooked_gudgeon()

    def craft_all_potions(self):
        """
        Cycles through all available recipes and crafts all items
        Starting with the highest level requirement, as the small HP potion eats all sunflowers
        :return:
        """
        self.get_skills_lvl()

        if self.alchemy <= 20:
            self.craft_earth_boost_potion()
        if self.alchemy <= 15:
            self.craft_small_hp_potion()

    def craft_all_weapons(self):
        """
        Goes through all weapon recipes and crafts all items
        Starting with the highest level requirement recipes
        """
        self.get_skills_lvl()

        # Lv1-4 Recipes
        if self.weaponcrafting < 5:
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Crafting Lv1-4 weapons..", "magenta"))
            self.craft_weapon_copper_dagger(recycle=True)
            self.craft_weapon_apprentice_gloves(recycle=True)
            self.craft_weapon_fishing_net(recycle=True)


    def craft_all_gear(self):
        """
        Goes through all gear recipes and crafts all items
        Starting with the highest level requirement recipes
        """
        self.get_skills_lvl()

        #Lv1-4 Recipes
        if self.gearcrafting < 5:
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Crafting Lv1-4 gear..", "magenta"))
            self.craft_gear_copper_boots(recycle=True)
            self.craft_gear_wooden_shield(recycle=True)

        # Lv5-10 Recipes
        if 4 < self.gearcrafting < 10:
            print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Crafting Lv5-10 gear..", "magenta"))
            self.craft_gear_copper_armor(recycle=True)


    def craft_copper_bars(self):
        """
        Craft copper bars in the Mining Workshop (1, 5)
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft copper bars...", "magenta"))
        copper_bars_recipe = [("copper_ore", 100)]
        self.craft_loop(self.ws_mining_coords, copper_bars_recipe, "copper_bar", 10)

    def craft_iron_bars(self):
        """
        Craft iron bars in the Mining Workshop (1, 5)
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft iron bars...", "magenta"))
        iron_bars_recipe = [("iron_ore", 100)]
        self.craft_loop(self.ws_mining_coords, iron_bars_recipe, "iron_bar", 10)

    def craft_ash_planks(self):
        """
        Craft ash planks in the Woodcutting Workshop (-2, -3)
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft ash planks...", "magenta"))
        ash_planks_recipe = [("ash_wood", 100)]
        self.craft_loop(self.ws_woodcutting_coords, ash_planks_recipe, "ash_plank", 10)

    def craft_spruce_planks(self):
        """
        Craft spruce planks in the Woodcutting Workshop (-2, -3)
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Spruce Planks...", "magenta"))
        spruce_planks_recipe = [("spruce_wood", 100)]
        self.craft_loop(self.ws_woodcutting_coords, spruce_planks_recipe, "spruce_plank", 10)

    def craft_cooked_gudgeon(self):
        """
        Cook gudgeon fish in the Cooking Workshop (1, 1)
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Cooked Gudgeon...", "magenta"))
        cooked_gudgeon_recipe = [("gudgeon", 100)]
        self.craft_loop(self.ws_cooking_coords, cooked_gudgeon_recipe, "cooked_gudgeon", 100)

    def craft_cooked_chicken(self):
        """
        Cook chicken in the Cooking Workshop (1, 1)
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Cooked Chicken...", "magenta"))
        cooked_chicken_recipe = [("raw_chicken", 100)]
        self.craft_loop(self.ws_cooking_coords, cooked_chicken_recipe, "cooked_chicken", 100 )

    def craft_small_hp_potion(self):
        """
        Crafting small HP Potion in the Alchemy Workshop (2, 3)
        Needs appropriate Alchemy Gathering level 5+
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Small HP Potions...", "magenta"))
        small_hp_potion_recipe = [("sunflower", 99)]
        self.craft_loop(self.ws_alchemy_coords, small_hp_potion_recipe, "small_health_potion", 33)

    def craft_earth_boost_potion(self):
        """
        Crafting small HP Potion in the Alchemy Workshop (2, 3)
        Needs appropriate Alchemy Gathering level 10+
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Earth Boost Potions...", "magenta"))
        earth_boost_potion_recipe = [("sunflower", 33), ("yellow_slimeball", 33), ("algae", 33)]
        self.craft_loop(self.ws_alchemy_coords, earth_boost_potion_recipe, "earth_boost_potion", 33)

    def craft_weapon_copper_dagger(self, recycle=False):
        """
        Crafting Copper Daggers in the Weaponcrafting Workshop (2, 1)
        Should only be crafted at levels 1-4
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Copper Daggers...", "magenta"))
        copper_dagger_recipe = [("copper_bar", 90)]
        self.craft_loop(self.ws_weaponcrafting_coords, copper_dagger_recipe, "copper_dagger", 15, recycle=recycle)

    def craft_weapon_apprentice_gloves(self, recycle=False):
        """
        Crafting Apprentice Gloves in the Weaponcrafting Workshop (2, 1)
        Should only be crafted at levels 1-4
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Apprentice Gloves...", "magenta"))
        apprentive_gloves_recipe = [("feather", 90)]
        self.craft_loop(self.ws_weaponcrafting_coords, apprentive_gloves_recipe, "apprentice_gloves", 15, recycle=recycle)

    def craft_weapon_fishing_net(self, recycle=False):
        """
        Crafting Fishing Net in the Weaponcrafting Workshop (2, 1)
        Should only be crafted at levels 1-4
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Fishing Net...", "magenta"))
        fishing_net_recipe = [("ash_plank", 90)]
        self.craft_loop(self.ws_weaponcrafting_coords, fishing_net_recipe, "fishing_net", 15, recycle=recycle)

    def craft_gear_copper_boots(self, recycle=False):
        """
        Crafting Copper Boots in the Gearcrafting Workshop (3, 1)
        Should only be crafted at levels 1-4
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Copper Boots...", "magenta"))
        copper_boots_recipe = [("copper_bar", 80)]
        self.craft_loop(self.ws_gearcrafting_coords, copper_boots_recipe, "copper_boots", 10, recycle=recycle)

    def craft_gear_wooden_shield(self, recycle=False):
        """
        Crafting Wooden Shields in the Gearcrafting Workshop (3, 1)
        Should only be crafted at levels 1-4
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Wooden Shields...", "magenta"))
        wooden_shield_recipe = [("ash_plank", 90)]
        self.craft_loop(self.ws_gearcrafting_coords, wooden_shield_recipe, "wooden_shield", 15, recycle=recycle)

    def craft_gear_copper_armor(self, recycle=False):
        """
        Crafting Copper Armors in the Gearcrafting Workshop (3, 1)
        Should only be crafted at levels 5-10
        Stop when withdrawing materials from bank doesnt work
        """
        print(f"[{self.name}][{self.time()}]: " + self.color_text(f"Starting to craft Copper Armors...", "magenta"))
        copper_armor_recipe = [("copper_bar", 75), ("wool", 25)]
        self.craft_loop(self.ws_gearcrafting_coords, copper_armor_recipe, "copper_armor", 15, recycle=recycle)

    def craft_loop(self, ws_coords, inputs, output, output_qty, recycle=False):
        """
        :param recycle: if ``true`` , immediately recycle items after crafting them
        :param ws_coords: workshop coordinates to craft at
        :param inputs: list of tuples (item_code, qty)
        :param output: output item code
        :param output_qty: quantity of output item
        """
        while True:
            self.move(*self.bank_coords)
            self.deposit()

            all_withdrawn = True
            for item_code, qty in inputs:
                if not self.withdraw(item_code, qty):
                    all_withdrawn = False
                    break

            if not all_withdrawn:
                self.deposit()
                break

            self.move(*ws_coords)
            self.craft(output, output_qty)
            if recycle:
                self.recycle(output, output_qty)

    def get_skills_lvl(self):
        data = self.get_character_data()
        combat = data["data"][0]["level"]
        mining = data["data"][0]["mining_level"]
        woodcutting = data["data"][0]["woodcutting_level"]
        fishing = data["data"][0]["fishing_level"]
        weaponcrafting = data["data"][0]["weaponcrafting_level"]
        gearcrafting = data["data"][0]["gearcrafting_level"]
        jewelrycrafting = data["data"][0]["jewelrycrafting_level"]
        cooking = data["data"][0]["cooking_level"]
        alchemy = data["data"][0]["alchemy_level"]

        self.combat = combat
        self.mining = mining
        self.woodcutting = woodcutting
        self.fishing = fishing
        self.weaponcrafting = weaponcrafting
        self.gearcrafting = gearcrafting
        self.jewelrycrafting = jewelrycrafting
        self.cooking = cooking
        self.alchemy = alchemy





if __name__ == '__main__':
    pass
    BlueMaiden = Player("BlueMaiden")
    BlueMaiden.recycle("copper_dagger", 1)
    # move("BlueMaiden", 0, 1)
    # fight("BlueMaiden")
    # rest("BlueMaiden")
