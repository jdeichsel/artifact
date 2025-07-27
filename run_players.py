import ast
import player
import argparse


def crafting_alchemy(player):
    print(f"[{player.name}] Starting to craft all alchemy items")
    player.craft_all_potions()


def crafting_mining(player):
    print(f"[{player.name}] Starting to craft all mining items")
    player.craft_all_bars()


def crafting_wood(player):
    print(f"[{player.name}] Starting to craft all wood items")
    player.craft_all_planks()


def crafting_fishing(player):
    print(f"[{player.name}] Starting to craft all fishing items")
    player.craft_all_food()


def fighting(player):
    print(f"[{player.name}] Starting to fight")
    player.fight_loop()


def gathering(player):
    print(f"[{player.name}] Starting to gather materials")
    player.gather_loop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="What character is supposed to do which action?")
    parser.add_argument('--player', type=str, help='Name of the player (BlueMaiden, WoodenMaiden, MiningMaiden, FishMaiden, AlchMaiden)')
    parser.add_argument('--action', type=str, help='Name of the action to do (fight, mining, wood, fishing, alchemy)')
    parser.add_argument('--coords', type=str, help='At what coordinate to do the action (0,0)')
    args = parser.parse_args()

    # workaround for scuffed tuple input as string
    if args.coords:
        coords = ast.literal_eval(args.coords)  # converts string "(0,1)" to tuple (0, 1)
    else:
        print("Invalid coords")
        raise ValueError

    player = player.Player(args.player)
    player.coords = coords
    player.role = args.action

    if args.action == "fight":
        fighting(player)
    elif args.action == "mining":
        crafting_mining(player)
        gathering(player)
    elif args.action == "wood":
        crafting_wood(player)
        gathering(player)
    elif args.action == "fishing":
        crafting_fishing(player)
        gathering(player)
    elif args.action == "alchemy":
        crafting_alchemy(player)
        gathering(player)
    else:
        print("Invalid action")
        raise ValueError






