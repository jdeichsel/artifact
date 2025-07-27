import ast
import player
import argparse


def crafting(player):
    print(f"[{player.name}] Starting to craft")
    player.craft_copper_bars()
    player.craft_ash_planks()

# EDGE CASE: only characters with alchemy level can do alchemy crafting
def crafting_alchemy(player):
    print(f"[{player.name}] Starting to craft alchemy items")
    player.craft_small_hp_potion()


def fighting(player):
    print(f"[{player.name}] Starting to fight")
    player.fight_loop()


def gathering(player):
    print(f"[{player.name}] Starting to gather")
    player.gather_loop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="What character is supposed to do which action?")
    parser.add_argument('--player', type=str, help='Name of the player (BlueMaiden, WoodenMaiden, MiningMaiden, FishMaiden, AlchMaiden)')
    parser.add_argument('--action', type=str, help='Name of the action to do (fight, gather, alchemy)')
    parser.add_argument('--coords', type=str, help='At what coordinate to do the action (0,0)')
    args = parser.parse_args()

    # workaround for scuffed tuple input as string
    if args.coords:
        coords = ast.literal_eval(args.coords)  # converts string "(0,1)" to tuple (0, 1)
    else:
        coords = (0, 0)  # default

    player = player.Player(args.player)
    player.coords = coords

    if args.action == "fight":
        crafting(player)
        fighting(player)
    elif args.action == "gather":
        gathering(player)
    else: # "alchemy"
        crafting_alchemy(player)
        gathering(player)






