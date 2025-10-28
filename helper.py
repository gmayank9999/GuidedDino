# # helper.py
# import math

# def oracle_action(state):
#     """
#     Heuristic oracle for the Dino game.
#     state = (distance_to_obstacle, obstacle_height, speed, y_position)
#     Returns 'jump', 'duck', or 'none'
#     """
#     d, h, v, y = state

#     # Safe heuristic thresholds
#     if d < 120 and h > 40:
#         return "jump"
#     elif d < 100 and h <= 40:
#         return "duck"
#     else:
#         return "none"

# # helper.py
# # Oracle helper returns integer actions:
# # 0 = noop, 1 = jump, 2 = duck

# def oracle_action(state):
#     """
#     state: (d, h, v, y, is_jumping) preferred
#     Also accepts (d,h,v,y) for backwards compatibility.
#     """
#     try:
#         d, h, v, y, is_jumping = state
#     except Exception:
#         d, h, v, y = state
#         is_jumping = False

#     # thresholds (tune these)
#     JUMP_DIST = 140
#     DUCK_DIST = 70
#     TALL = 45

#     # never tell to duck while mid-air
#     if is_jumping:
#         return 0

#     # prefer jump for tall obstacles
#     if d < JUMP_DIST and h >= TALL:
#         return 1

#     # duck only for short obstacle very close
#     if d < DUCK_DIST and h < TALL:
#         return 2

#     return 0



# # helper.py
# # Oracle helper returns integer actions:
# # 0 = noop, 1 = jump, 2 = duck

# def oracle_action(state):
#     """
#     state: (d, h, speed, y, is_jumping, obst_type)
#     obst_type: 'ground' or 'air' (string)
#     Returns 0/1/2
#     """
#     try:
#         d, h, v, y, is_jumping, obst_type = state
#     except Exception:
#         # Backwards compatibility: handle (d,h,v,y,is_jumping) or (d,h,v,y)
#         try:
#             d, h, v, y, is_jumping = state
#             obst_type = 'ground'
#         except Exception:
#             d, h, v, y = state
#             is_jumping = False
#             obst_type = 'ground'

#     # Tunable thresholds
#     JUMP_DIST = 140    # distance threshold to prepare jump for tall ground obstacles
#     DUCK_DIST = 110    # distance threshold to duck for air obstacles
#     TALL_HEIGHT = 45   # obstacle height above which jumping is needed

#     # If player is mid-air, don't instruct duck
#     if is_jumping:
#         return 0

#     # If upcoming obstacle is an 'air' type (flying), prefer duck if close enough
#     if obst_type == 'air':
#         if d < DUCK_DIST:
#             return 2  # duck
#         else:
#             return 0

#     # For ground obstacles:
#     # If tall ground obstacle (height >= TALL_HEIGHT) and within JUMP_DIST -> jump
#     if obst_type == 'ground':
#         if d < JUMP_DIST and h >= TALL_HEIGHT:
#             return 1  # jump
#         # if very close and small height (rare), we can duck as defensive but safer to jump
#         if d < 40 and h < TALL_HEIGHT:
#             return 1  # jump (prefer jump)
#     return 0


# # helper.py
# # Oracle helper returns integer actions:
# # 0 = noop, 1 = jump, 2 = duck

# def oracle_action(state):
#     """
#     state: (d, h, speed, y, is_jumping, obst_type)
#     obst_type: 'ground' or 'air' (string)
#     Returns 0/1/2
#     """
#     try:
#         d, h, v, y, is_jumping, obst_type = state
#     except Exception:
#         # Backwards compatibility: handle (d,h,v,y,is_jumping) or (d,h,v,y)
#         try:
#             d, h, v, y, is_jumping = state
#             obst_type = 'ground'
#         except Exception:
#             d, h, v, y = state
#             is_jumping = False
#             obst_type = 'ground'

#     # === IMPROVED DYNAMIC THRESHOLDS ===
#     # Scale reaction distance with speed (faster = need more time)
#     base_reaction_time = 25  # frames to react
#     reaction_distance = v * base_reaction_time
    
#     # Duck is better for low obstacles, jump for tall ones
#     DUCK_HEIGHT_THRESHOLD = 25  # obstacles <= this height should be ducked
#     TALL_HEIGHT = 35            # obstacles >= this height must be jumped
    
#     # Early duck distance for air obstacles (they need more prep time)
#     AIR_DUCK_DISTANCE = reaction_distance * 1.4
#     GROUND_DUCK_DISTANCE = reaction_distance * 0.9
#     JUMP_DISTANCE = reaction_distance * 1.2

#     # === DECISION LOGIC ===
    
#     # If player is mid-air, don't give instructions
#     if is_jumping:
#         return 0

#     # === AIR OBSTACLES (flying) ===
#     if obst_type == 'air':
#         if d < AIR_DUCK_DISTANCE:
#             return 2  # duck - air obstacles ALWAYS need ducking
#         else:
#             return 0

#     # === GROUND OBSTACLES ===
#     if obst_type == 'ground':
        
#         # Small/short obstacles - DUCK is better (faster recovery)
#         if h <= DUCK_HEIGHT_THRESHOLD:
#             if d < GROUND_DUCK_DISTANCE:
#                 return 2  # duck
#             else:
#                 return 0
        
#         # Tall obstacles - MUST JUMP
#         elif h >= TALL_HEIGHT:
#             if d < JUMP_DISTANCE:
#                 return 1  # jump
#             else:
#                 return 0
        
#         # Medium height (25-35) - prefer jump but duck works too
#         else:
#             if d < reaction_distance:
#                 return 1  # safer to jump for medium obstacles
#             else:
#                 return 0

#     return 0  # default: do nothing

# helper.py
# Oracle helper returns integer actions:
# 0 = noop, 1 = jump, 2 = duck

def oracle_action(state):
    """
    state: (d, h, speed, y, is_jumping, obst_type, obstacle_y)
    
    d: distance to obstacle
    h: obstacle height
    speed: current game speed
    y: dino Y position
    is_jumping: whether dino is in air
    obst_type: 'ground' or 'air'
    obstacle_y: Y position of obstacle top
    
    Returns: 0 (nothing), 1 (jump), 2 (duck)
    """
    obstacle_y = None
    try:
        d, h, v, y, is_jumping, obst_type, obstacle_y = state
    except Exception:
        try:
            d, h, v, y, is_jumping, obst_type = state
        except Exception:
            # Backwards compatibility
            try:
                d, h, v, y, is_jumping = state
                obst_type = 'ground'
            except Exception:
                d, h, v, y = state
                is_jumping = False
                obst_type = 'ground'

    # === CONSTANTS ===
    GROUND_Y = 300
    DINO_STANDING_HEIGHT = 30
    DINO_DUCKING_HEIGHT = 18
    
    # === DYNAMIC THRESHOLDS (scale with speed) ===
    base_reaction_time = 25
    reaction_distance = v * base_reaction_time
    
    DUCK_HEIGHT_THRESHOLD = 25  # short ground obstacles
    TALL_HEIGHT = 35            # tall ground obstacles
    
    GROUND_DUCK_DISTANCE = reaction_distance * 0.9
    JUMP_DISTANCE = reaction_distance * 1.1

    # === IF MID-AIR, DO NOTHING ===
    if is_jumping:
        return 0

    # === AIR OBSTACLES (Flying) ===
    if obst_type == 'air':
        # Now with obstacle_y, we can make precise decisions!
        if obstacle_y is not None:
            obstacle_bottom = obstacle_y + h
            dino_standing_top = GROUND_Y - DINO_STANDING_HEIGHT
            
            # Check if air obstacle will hit standing dino
            # Air obstacle bottom > dino standing top = COLLISION!
            if obstacle_bottom >= dino_standing_top - 5:  # 5px safety margin
                # This air obstacle is LOW - will hit standing dino
                if d < reaction_distance * 1.3:  # Earlier reaction for air
                    return 2  # DUCK to avoid
            # Else: obstacle is high enough, passes over standing dino
            return 0
        else:
            # Fallback: if no Y info, assume air = duck (safer)
            if d < reaction_distance * 1.2:
                return 2
            return 0

    # === GROUND OBSTACLES ===
    if obst_type == 'ground':
        
        # Short obstacles - DUCK is efficient
        if h <= DUCK_HEIGHT_THRESHOLD:
            if d < GROUND_DUCK_DISTANCE:
                return 2  # duck
            return 0
        
        # Tall obstacles - MUST JUMP
        elif h >= TALL_HEIGHT:
            if d < JUMP_DISTANCE:
                return 1  # jump
            return 0
        
        # Medium height (25-35) - prefer jump
        else:
            if d < reaction_distance:
                return 1  # jump
            return 0

    return 0