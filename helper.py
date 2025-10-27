# helper.py
import math

def oracle_action(state):
    """
    Heuristic oracle for the Dino game.
    state = (distance_to_obstacle, obstacle_height, speed, y_position)
    Returns 'jump', 'duck', or 'none'
    """
    d, h, v, y = state

    # Safe heuristic thresholds
    if d < 120 and h > 40:
        return "jump"
    elif d < 100 and h <= 40:
        return "duck"
    else:
        return "none"
