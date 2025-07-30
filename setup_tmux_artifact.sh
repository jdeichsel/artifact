SESSION="artifact"

tmux new-session -d -s $SESSION

declare -a PLAYERS=("BlueMaiden" "WoodenMaiden" "MiningMaiden" "FishMaiden" "AlchMaiden")
ACTIONS=("fight" "wood" "mining" "fishing" "alchemy")
COORDS=("(2, -1)" "(-1, 6)" "(1, 6)" "(7, 12)" "(7, 14)")

for i in "${!PLAYERS[@]}"; do
    tmux new-window -t $SESSION: -n "${PLAYERS[i]}"
    tmux send-keys -t $SESSION:"${PLAYERS[i]}" \
        "python /home/jan/_py/artifact/run_players.py --player ${PLAYERS[i]} --action ${ACTIONS[i]} --coords '${COORDS[i]}'" C-m
done





# (Lv1) fight: chicken: (0, 1)
# (Lv2) fight: yellow slime: (1, -2)
# (Lv5) fight: sheep: (5, 12)
# (Lv6) fight: blue slime: (2, -1)


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
# (Lv35) wood: magic tree: (3, 11)
# (Lv40) wood: maple tree: (4, 14)

