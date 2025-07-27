import ast
import player
import argparse


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
        gathering(player)
    elif args.action == "wood":
        gathering(player)
    elif args.action == "fishing":
        gathering(player)
    elif args.action == "alchemy":
        gathering(player)
    else:
        print("Invalid action")
        raise ValueError






