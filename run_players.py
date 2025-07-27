import ast
import player
import argparse


# (Lv1) fight: chicken: (0, 1)
# (Lv2) fight: yellow slime: (1, -2)


# (Lv1) fishing: gudgeon: (4, 2)
# (Lv10) fishing: shrimp: (5, 2)
# (Lv20) fishing: trout: (7, 12)
# (Lv30) fishing: bass: (6, 12)
# (Lv40) fishing: salmon: (-2, -4)

# (Lv1) alchemy: sunflower: (2, 2)
# (Lv20) alchemy: nettle: (7, 14)
# (Lv40) alchemy: glowstem: (1, 10)

# (Lv1) mining: copper: (2, 0)
# (Lv10) mining: iron: (1, 7)
# (Lv20) mining: coal: (1, 6)
# (Lv30) mining: gold: (6, -3)
# (Lv35) mining: strange rocks: (9, 11)
# (Lv40) mining: mithril: (-2, 13)

# (Lv1) wood: ash tree: (-1, 0)
# (Lv10) wood: spruce tree: (1, 9)
# (Lv20) wood: birch tree: (-1, 6)
# (Lv30) wood: dead tree: (9, 8)
# (Lv40) wood: maple tree: (4, 14)





def fighting(player):
    print(f"[{player.name}] Starting to fight")
    player.fight_loop()

def gathering(player):
    print(f"[{player.name}] Starting to gather")
    player.gather_loop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="What character is supposed to do which action?")
    parser.add_argument('--player', type=str, help='Name of the player (BlueMaiden, WoodenMaiden, MiningMaiden, FishMaiden, AlchMaiden)')
    parser.add_argument('--action', type=str, help='Name of the action to do (fight, gather)')
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
        fighting(player)
    else:
        gathering(player)






