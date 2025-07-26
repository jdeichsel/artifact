import player
import threading
import argparse


# (Lv1) fight chicken: (0, 1)
# (Lv1) gather copper: (2, 0)
# (Lv1) gather ash tree: (-1, 0)
# (Lv1) gather gudgeon fish: (4, 2)
# (Lv1) gather sunflower: (2, 2)

# Combat Lv1
def fighting(player):
    print(f"[{player.name}] Starting to fight")
    player.coords = args.coords
    player.fight_loop()

# Gather Lv1
def gathering(player):
    print(f"[{player.name}] Starting to gather")
    player.coords = args.coords
    player.gather_loop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="What character is supposed to do which action?")
    parser.add_argument('--player', type=str, help='Name of the player (BlueMaiden, WoodenMaiden, MiningMaiden, FishMaiden, AlchMaiden)')
    parser.add_argument('--action', type=str, help='Name of the action to do (fight, gather)')
    parser.add_argument('--coords', type=tuple, help='At what coordinate to do the action (0,0)')
    args = parser.parse_args()

    player = player.Player(args.player)

    if args.action == "fight":
        fighting(player)
    else:
        gathering(player)






