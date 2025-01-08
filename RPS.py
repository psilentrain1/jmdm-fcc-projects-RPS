from itertools import product
import random

LOOKBACK: int = 5
RETENTION: int = 1000
STARTING_MOVE: str = "R"
MOVES: list[str] = ["R", "P", "S"]
WINNING_PLAYS: dict[str, str] = {"R": "P", "P": "S", "S": "R"}
player_history: list[str] = []
opponent_history: list[str] = []
play_order: dict[str, int] = {
    "".join(combo): 0 for combo in product(MOVES, repeat=LOOKBACK)
}


def player(prev_play: str) -> str:
    global player_history
    global opponent_history
    global play_order

    # Delete history after *n moves
    if len(opponent_history) >= RETENTION:
        opponent_history = []
        player_history = []

    # Use a value for the first row of data
    if not prev_play:
        prev_play = "R"

    opponent_history.append(prev_play)

    guess: str = STARTING_MOVE
    if len(opponent_history) > 2 and len(opponent_history) < LOOKBACK:
        guess = opponent_history[-2]
    elif len(opponent_history) > LOOKBACK:
        past_plays = "".join(opponent_history[LOOKBACK * -1 :])
        play_order[past_plays] = play_order.get(past_plays, 0) + 1

        potential_plays = [
            "".join([*opponent_history[(LOOKBACK - 1) * -1 :], p]) for p in MOVES
        ]

        sub_order = {k: play_order[k] for k in potential_plays if k in play_order}

        if sub_order:
            prediction = max(sub_order, key=sub_order.get)[-1:]

        guess = WINNING_PLAYS[prediction]

    player_history.append(guess)
    return guess
