import player
import threading



# Combat Lv1
def fight_chickens(player):
    print(f"[{player.name}] Fighting chickens")
    player.move(0, 1)
    player.fight_loop()

# Gather Lv1
def gather_copper(player):
    print(f"[{player.name}] Gathering copper")
    player.coords = (2, 0)
    player.gather_loop()

# Gather Lv1
def gather_ash_tree(player):
    print(f"[{player.name}] Gathering ash tree")
    player.coords = (-1, 0)
    player.gather_loop()

# Gather Lv1
def gather_gudgeon_fish(player):
    print(f"[{player.name}] Gathering gudgeon fish")
    player.coords = (4, 2)
    player.gather_loop()

# Gather Lv1
def gather_sunflower(player):
    print(f"[{player.name}] Gathering sunflowers")
    player.coords = (2, 2)
    player.gather_loop()




if __name__ == '__main__':
    BlueMaiden = player.Player("BlueMaiden")
    WoodenMaiden = player.Player("WoodenMaiden")
    MiningMaiden = player.Player("MiningMaiden")
    FishMaiden = player.Player("FishMaiden")
    AlchMaiden = player.Player("AlchMaiden")


    BlueMaiden_thread = threading.Thread(target=fight_chickens, args=(BlueMaiden,))
    BlueMaiden_thread.daemon = False
    BlueMaiden_thread.start()

    WoodenMaiden_thread = threading.Thread(target=gather_ash_tree, args=(WoodenMaiden,))
    WoodenMaiden_thread.daemon = False
    WoodenMaiden_thread.start()

    MiningMaiden_thread = threading.Thread(target=gather_copper, args=(MiningMaiden,))
    MiningMaiden_thread.daemon = False
    MiningMaiden_thread.start()

    FishMaiden_thread = threading.Thread(target=gather_gudgeon_fish, args=(FishMaiden,))
    FishMaiden_thread.daemon = False
    FishMaiden_thread.start()

    AlchMaiden_thread = threading.Thread(target=gather_sunflower, args=(AlchMaiden,))
    AlchMaiden_thread.daemon = False
    AlchMaiden_thread.start()





