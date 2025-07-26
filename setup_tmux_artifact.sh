SESSION="artifact"

tmux new-session -d -s $SESSION

declare -a PLAYERS=("BlueMaiden" "WoodenMaiden" "MiningMaiden" "FishMaiden" "AlchMaiden")
ACTIONS=("fight" "gather" "gather" "gather" "gather")
COORDS=("(1, -2)" "(-1, 0)" "(2, 0)" "(4, 2)" "(2, 2)")

for i in "${!PLAYERS[@]}"; do
    tmux new-window -t $SESSION: -n "${PLAYERS[i]}"
    tmux send-keys -t $SESSION:"${PLAYERS[i]}" \
        "python /home/jan/_py/artifact/run_players.py --player ${PLAYERS[i]} --action ${ACTIONS[i]} --coords '${COORDS[i]}'" C-m
done

