# # game.py
# import pygame
# import random
# from helper import oracle_action

# pygame.init()

# # Constants
# WIDTH, HEIGHT = 800, 300
# GROUND_Y = 250
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (230, 230, 230)

# # Dino class
# class Dino:
#     def __init__(self):
#         self.x = 50
#         self.y = GROUND_Y
#         self.vel_y = 0
#         self.is_jumping = False
#         self.is_ducking = False

#     def jump(self):
#         if not self.is_jumping:
#             self.vel_y = -10
#             self.is_jumping = True

#     def duck(self):
#         self.is_ducking = True

#     def unduck(self):
#         self.is_ducking = False

#     def update(self):
#         if self.is_jumping:
#             self.y += self.vel_y
#             self.vel_y += 0.5
#             if self.y >= GROUND_Y:
#                 self.y = GROUND_Y
#                 self.is_jumping = False

#     def draw(self, screen):
#         color = (0, 100, 200)
#         rect = pygame.Rect(self.x, self.y - (30 if not self.is_ducking else 10), 30, 30)
#         pygame.draw.rect(screen, color, rect)

# # Obstacle class
# class Obstacle:
#     def __init__(self, x):
#         self.x = x
#         self.h = random.choice([30, 50, 70])
#         self.w = 20

#     def update(self, speed):
#         self.x -= speed

#     def draw(self, screen):
#         pygame.draw.rect(screen, (200, 50, 50), (self.x, GROUND_Y - self.h, self.w, self.h))

# # Main game
# def main():
#     screen = pygame.display.set_mode((WIDTH, HEIGHT))
#     pygame.display.set_caption("Guided Dino Game")

#     clock = pygame.time.Clock()
#     dino = Dino()
#     obstacles = [Obstacle(600)]
#     running = True
#     helper_on = True
#     speed = 6
#     score = 0

#     while running:
#         clock.tick(30)
#         screen.fill(WHITE)
#         pygame.draw.line(screen, GRAY, (0, GROUND_Y + 1), (WIDTH, GROUND_Y + 1), 2)

#         # Spawn obstacles
#         if len(obstacles) == 0 or obstacles[-1].x < 400:
#             obstacles.append(Obstacle(WIDTH + random.randint(100, 300)))

#         # Game events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     dino.jump()
#                 elif event.key == pygame.K_DOWN:
#                     dino.duck()
#                 elif event.key == pygame.K_h:
#                     helper_on = not helper_on
#                     print("Helper:", helper_on)
#             elif event.type == pygame.KEYUP:
#                 if event.key == pygame.K_DOWN:
#                     dino.unduck()

#         # Update
#         dino.update()
#         for obs in obstacles:
#             obs.update(speed)
#         obstacles = [o for o in obstacles if o.x + o.w > 0]

#         # AI Helper suggestion
#         if helper_on and obstacles:
#             obs = obstacles[0]
#             state = (obs.x - dino.x, obs.h, speed, dino.y)
#             act = oracle_action(state)
#             if act == "jump":
#                 dino.jump()
#             elif act == "duck":
#                 dino.duck()
#             else:
#                 dino.unduck()

#         # Collision detection
#         for obs in obstacles:
#             if obs.x < dino.x + 30 and obs.x + obs.w > dino.x and dino.y > GROUND_Y - obs.h:
#                 print("Game Over! Final Score:", score)
#                 running = False

#         # Draw
#         dino.draw(screen)
#         for obs in obstacles:
#             obs.draw(screen)

#         score += 1
#         pygame.display.flip()

#     pygame.quit()

# if __name__ == "__main__":
#     print("# Controls: SPACE=jump, DOWN=duck, H=toggle helper")
#     main()


# # game.py
# import pygame
# import random
# import time

# # optional logger import (if present)
# try:
#     from logger import RunLogger
# except Exception:
#     RunLogger = None

# from helper import oracle_action  # expects state (d,h,speed,y,is_jumping) -> 0/1/2

# pygame.init()

# # Constants
# WIDTH, HEIGHT = 900, 320
# GROUND_Y = 260
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (230, 230, 230)
# FPS = 30

# # Dino with jump + duck duration
# class Dino:
#     def __init__(self):
#         self.x = 50
#         self.y = GROUND_Y
#         self.vel_y = 0
#         self.is_jumping = False
#         self.is_ducking = False
#         self.duck_timer = 0
#         self.DUCK_DURATION = int(0.6 * FPS)

#     def jump(self):
#         if not self.is_jumping and not self.is_ducking:
#             self.vel_y = -12
#             self.is_jumping = True

#     def duck(self):
#         if not self.is_jumping and not self.is_ducking:
#             self.is_ducking = True
#             self.duck_timer = self.DUCK_DURATION

#     def unduck(self):
#         self.is_ducking = False
#         self.duck_timer = 0

#     def update(self):
#         # jumping physics
#         if self.is_jumping:
#             self.y += self.vel_y
#             self.vel_y += 0.7
#             if self.y >= GROUND_Y:
#                 self.y = GROUND_Y
#                 self.is_jumping = False
#                 self.vel_y = 0
#         # duck timer
#         if self.is_ducking:
#             self.duck_timer -= 1
#             if self.duck_timer <= 0:
#                 self.unduck()

#     def get_rect(self):
#         h = 20 if self.is_ducking else 30
#         return pygame.Rect(self.x, self.y - h, 30, h)

#     def draw(self, screen):
#         pygame.draw.rect(screen, (0, 100, 200), self.get_rect())

# # Obstacle
# class Obstacle:
#     def __init__(self, x, w=None, h=None):
#         self.x = x
#         self.w = 20 if w is None else w
#         self.h = random.choice([20, 30, 40, 60]) if h is None else h

#     def update(self, speed):
#         self.x -= speed

#     def get_rect(self):
#         return pygame.Rect(self.x, GROUND_Y - self.h, self.w, self.h)

#     def draw(self, screen):
#         pygame.draw.rect(screen, (200, 50, 50), self.get_rect())

# # Main game class
# class DinoGame:
#     def __init__(self, helper_on=True, auto_mode=False, logger=None):
#         self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
#         pygame.display.set_caption("Guided Dino")
#         self.clock = pygame.time.Clock()
#         self.dino = Dino()
#         self.obstacles = []
#         self.spawn_timer = 0
#         self.speed = 6
#         self.score = 0
#         self.helper_on = helper_on
#         self.auto_mode = auto_mode
#         self.hint = None
#         self.logger = logger
#         self.step_idx = 0

#     def reset(self):
#         self.dino = Dino()
#         self.obstacles = []
#         self.spawn_timer = 0
#         self.score = 0
#         self.hint = None
#         self.step_idx = 0
#         self.speed = 6

#     def spawn_obstacle(self):
#         gap = random.randint(100, 300)
#         x = WIDTH + gap
#         w = random.choice([18, 20, 24])
#         h = random.choice([20, 30, 40, 60])
#         self.obstacles.append(Obstacle(x, w=w, h=h))

#     def get_state(self):
#         if self.obstacles:
#             obs = min(self.obstacles, key=lambda o: o.x)
#             d = obs.x - self.dino.x
#             h = obs.h
#         else:
#             d, h = WIDTH, 0
#         return (d, h, self.speed, self.dino.y, self.dino.is_jumping)

#     def step(self, player_action):
#         # apply player action (0 noop,1 jump,2 duck)
#         if player_action == 1:
#             self.dino.jump()
#         elif player_action == 2:
#             self.dino.duck()

#         self.dino.update()
#         for o in self.obstacles:
#             o.update(self.speed)
#         self.obstacles = [o for o in self.obstacles if o.x + o.w > -50]

#         self.spawn_timer += 1
#         if self.spawn_timer > int(0.8 * FPS):
#             self.spawn_timer = 0
#             if random.random() < 0.75:
#                 self.spawn_obstacle()

#         # collision
#         dino_rect = self.dino.get_rect()
#         for o in self.obstacles:
#             if dino_rect.colliderect(o.get_rect()):
#                 return False

#         # score & difficulty
#         self.score += 1
#         if self.score % 500 == 0:
#             self.speed += 1
#         return True

#     def log_step(self, state, player_action, oracle_action):
#         # logger signature: log_step(state, player_action, oracle_action, helper_on, score)
#         if not self.logger:
#             return
#         try:
#             self.logger.log_step(state, player_action, oracle_action, int(self.helper_on), int(self.score))
#         except TypeError:
#             # fallback - some older logger versions may have slightly different arg order
#             try:
#                 self.logger.log_step(state, player_action, oracle_action, int(self.helper_on), int(self.score))
#             except Exception:
#                 pass

#     def draw(self):
#         self.screen.fill(WHITE)
#         pygame.draw.line(self.screen, GRAY, (0, GROUND_Y + 1), (WIDTH, GROUND_Y + 1), 2)
#         self.dino.draw(self.screen)
#         for o in self.obstacles:
#             o.draw(self.screen)
#         # helper hint
#         if self.hint is not None and self.helper_on:
#             txt = ""
#             if self.hint == 1: txt = "JUMP"
#             elif self.hint == 2: txt = "DUCK"
#             font = pygame.font.SysFont(None, 28)
#             surf = font.render(txt, True, (0, 0, 255))
#             self.screen.blit(surf, (self.dino.x + 40, self.dino.y - 50))
#         # score & HUD
#         font2 = pygame.font.SysFont(None, 22)
#         s = font2.render(f"Score: {self.score}  Speed: {self.speed}  Helper: {'ON' if self.helper_on else 'OFF'}  Auto: {'ON' if self.auto_mode else 'OFF'}", True, BLACK)
#         self.screen.blit(s, (10, 8))
#         pygame.display.flip()

#     def run(self):
#         running = True
#         alive = True
#         while running and alive:
#             self.clock.tick(FPS)
#             player_action = 0
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                     alive = False
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_SPACE:
#                         player_action = 1
#                     elif event.key == pygame.K_DOWN:
#                         player_action = 2
#                     elif event.key == pygame.K_h:
#                         self.helper_on = not self.helper_on
#                     elif event.key == pygame.K_a:
#                         self.auto_mode = not self.auto_mode
#                 elif event.type == pygame.KEYUP:
#                     if event.key == pygame.K_DOWN:
#                         # manual unduck on keyup
#                         try:
#                             self.dino.unduck()
#                         except:
#                             pass

#             # helper suggestion
#             if self.helper_on:
#                 state = self.get_state()
#                 try:
#                     act = oracle_action(state)
#                 except Exception:
#                     # support older oracle signature
#                     act = oracle_action(state[:4])
#                 # normalize to int
#                 try:
#                     hint_num = int(act)
#                 except:
#                     if isinstance(act, str):
#                         hint_num = 1 if act.lower() == "jump" else (2 if act.lower() == "duck" else 0)
#                     else:
#                         hint_num = 0
#                 self.hint = hint_num
#                 # auto mode executes
#                 if self.auto_mode:
#                     if hint_num == 1:
#                         self.dino.jump()
#                     elif hint_num == 2:
#                         self.dino.duck()
#             else:
#                 self.hint = None

#             alive = self.step(player_action)

#             # logging
#             state_for_log = (self.get_state()[0], self.get_state()[1], self.get_state()[2], self.get_state()[3])
#             oracle_for_log = self.hint if self.hint is not None else -1
#             self.log_step(state_for_log, player_action, oracle_for_log)
#             self.step_idx += 1

#             self.draw()

#             if not alive:
#                 # show brief game over
#                 font = pygame.font.SysFont(None, 36)
#                 surf = font.render(f"Game Over! Final Score: {self.score}", True, BLACK)
#                 self.screen.blit(surf, (WIDTH // 2 - 200, HEIGHT // 2 - 20))
#                 pygame.display.flip()
#                 time.sleep(0.6)
#                 break

#         return self.score

# if __name__ == "__main__":
#     print("# Controls: SPACE=jump, DOWN=duck, H=toggle helper, A=toggle auto-mode")
#     logger = None
#     try:
#         if RunLogger is not None:
#             logger = RunLogger("data/runs/run_human_helper.csv")
#     except Exception:
#         logger = None

#     g = DinoGame(helper_on=True, auto_mode=False, logger=logger)
#     try:
#         while True:
#             s = g.run()
#             print("Run ended, score:", s)
#             try:
#                 if logger:
#                     logger.end_run(s)
#             except:
#                 pass
#             time.sleep(0.2)
#             g.reset()
#     except KeyboardInterrupt:
#         print("Exiting.")
#         if logger:
#             try:
#                 logger.close()
#             except:
#                 pass
#         pygame.quit()

# # game.py
# import pygame
# import random
# import time

# # optional logger import (if present)
# try:
#     from logger import RunLogger
# except Exception:
#     RunLogger = None

# from helper import oracle_action  # expects state (d,h,speed,y,is_jumping,obst_type)

# pygame.init()

# # Constants
# WIDTH, HEIGHT = 960, 360
# GROUND_Y = 300
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# GRAY = (230, 230, 230)
# FPS = 30

# # Dino with jump + duck duration
# class Dino:
#     def __init__(self):
#         self.x = 70
#         self.y = GROUND_Y
#         self.vel_y = 0
#         self.is_jumping = False
#         self.is_ducking = False
#         self.duck_timer = 0
#         self.DUCK_DURATION = int(0.5 * FPS)

#     def jump(self):
#         if not self.is_jumping and not self.is_ducking:
#             self.vel_y = -13
#             self.is_jumping = True

#     def duck(self):
#         if not self.is_jumping and not self.is_ducking:
#             self.is_ducking = True
#             self.duck_timer = self.DUCK_DURATION

#     def unduck(self):
#         self.is_ducking = False
#         self.duck_timer = 0

#     def update(self):
#         # gravity & jump physics
#         if self.is_jumping:
#             self.y += self.vel_y
#             self.vel_y += 0.8
#             if self.y >= GROUND_Y:
#                 self.y = GROUND_Y
#                 self.is_jumping = False
#                 self.vel_y = 0
#         # duck timer logic
#         if self.is_ducking:
#             self.duck_timer -= 1
#             if self.duck_timer <= 0:
#                 self.unduck()

#     def get_rect(self):
#         h = 18 if self.is_ducking else 30
#         return pygame.Rect(self.x, self.y - h, 34, h)

#     def draw(self, screen):
#         r = self.get_rect()
#         pygame.draw.rect(screen, (0, 120, 200), r)

# # Obstacle with type: 'ground' (on floor) or 'air' (flying)
# class Obstacle:
#     def __init__(self, x, typ='ground'):
#         self.x = x
#         self.w = random.choice([18, 22, 26])
#         self.type = typ
#         # heights: for ground -> variable height from ground
#         # for air -> lower heights (so Dino must duck)
#         if typ == 'ground':
#             self.h = random.choice([20, 30, 40, 60])  # tall ones need jump
#             self.y = GROUND_Y - self.h
#         else:  # 'air'
#             # air obstacles placed above ground by offset (so ducking helps)
#             self.h = random.choice([12, 16, 20])
#             self.y = GROUND_Y - 120 - random.randint(-10, 30)  # floating y
#         # random color per type
#         self.color = (200, 50, 50) if self.type == 'ground' else (150, 50, 200)

#     def update(self, speed):
#         self.x -= speed

#     def get_rect(self):
#         return pygame.Rect(self.x, self.y, self.w, self.h)

#     def draw(self, screen):
#         pygame.draw.rect(screen, self.color, self.get_rect())

# # Main game class
# class DinoGame:
#     def __init__(self, helper_on=True, auto_mode=False, logger=None):
#         self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
#         pygame.display.set_caption("Guided Dino")
#         self.clock = pygame.time.Clock()
#         self.dino = Dino()
#         self.obstacles = []
#         self.spawn_timer = 0
#         self.speed = 6
#         self.score = 0
#         self.helper_on = helper_on
#         self.auto_mode = auto_mode
#         self.hint = None
#         self.logger = logger
#         self.run_id = int(time.time())
#         self.step_idx = 0
#         self.high_score = 0

#     def reset(self):
#         if self.score > self.high_score:
#             self.high_score = self.score
#         self.dino = Dino()
#         self.obstacles = []
#         self.spawn_timer = 0
#         self.speed = 6
#         self.score = 0
#         self.hint = None
#         self.step_idx = 0

#     def spawn_obstacle(self):
#         gap = random.randint(160, 360)
#         x = WIDTH + gap
#         # decide type with some probability (air obstacles rarer)
#         typ = 'air' if random.random() < 0.18 else 'ground'
#         self.obstacles.append(Obstacle(x, typ=typ))

#     def get_nearest(self):
#         if not self.obstacles:
#             return None
#         return min(self.obstacles, key=lambda o: o.x)

#     def get_state(self):
#         nearest = self.get_nearest()
#         if nearest is None:
#             return (9999, 0, self.speed, self.dino.y, self.dino.is_jumping, 'ground')
#         d = nearest.x - self.dino.x
#         h = nearest.get_rect().height
#         return (d, h, self.speed, self.dino.y, self.dino.is_jumping, nearest.type)

#     def step(self, player_action):
#         # apply player action
#         if player_action == 1:
#             self.dino.jump()
#         elif player_action == 2:
#             self.dino.duck()
#         # physics update
#         self.dino.update()
#         for o in self.obstacles:
#             o.update(self.speed)
#         self.obstacles = [o for o in self.obstacles if o.x + o.w > -50]

#         # spawn logic
#         self.spawn_timer += 1
#         if self.spawn_timer > int(0.8 * FPS):
#             self.spawn_timer = 0
#             if random.random() < 0.7:
#                 self.spawn_obstacle()

#         # collision
#         dino_rect = self.dino.get_rect()
#         for o in self.obstacles:
#             if dino_rect.colliderect(o.get_rect()):
#                 return False

#         # scoring & speed ramp
#         self.score += 1
#         if self.score % 600 == 0:
#             self.speed += 1
#         return True

#     def log_step(self, state, player_action, oracle_action):
#         if not self.logger:
#             return
#         # state for logger: (d,h,speed,y)
#         try:
#             d,h,speed,y,_,_ = state
#         except:
#             d = state[0]; h = state[1]; speed = state[2]; y = state[3]
#         oa = -1 if oracle_action is None else oracle_action
#         try:
#             oa = int(oa)
#         except:
#             oa = -1
#         try:
#             self.logger.log_step((d, h, speed, y), player_action, oa, int(self.helper_on), int(self.score))
#         except Exception:
#             # fallback older signature
#             try:
#                 self.logger.log_step((d, h, speed, y), player_action, oa, int(self.helper_on), int(self.score))
#             except:
#                 pass

#     def draw_hud(self):
#         font = pygame.font.SysFont(None, 22)
#         text = f"Score: {self.score}  High: {self.high_score}  Speed: {self.speed}  Helper: {'ON' if self.helper_on else 'OFF'}  Auto: {'ON' if self.auto_mode else 'OFF'}"
#         surf = font.render(text, True, BLACK)
#         self.screen.blit(surf, (12, 8))

#     def draw(self):
#         self.screen.fill(WHITE)
#         # ground
#         pygame.draw.rect(self.screen, GRAY, (0, GROUND_Y + 1, WIDTH, HEIGHT - GROUND_Y))
#         # draw dino & obstacles
#         self.dino.draw(self.screen)
#         for o in self.obstacles:
#             o.draw(self.screen)
#         # helper hint
#         if self.hint is not None and self.helper_on:
#             txt = ""
#             if self.hint == 1: txt = "JUMP"
#             elif self.hint == 2: txt = "DUCK"
#             font = pygame.font.SysFont(None, 30)
#             surf = font.render(txt, True, (0, 0, 255))
#             # show above dino
#             self.screen.blit(surf, (self.dino.x + 40, self.dino.y - 60))
#         # HUD
#         self.draw_hud()
#         pygame.display.flip()

#     def run(self):
#         running = True
#         alive = True
#         while running and alive:
#             self.clock.tick(FPS)
#             player_action = 0
#             # input handling
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                     alive = False
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_SPACE:
#                         player_action = 1
#                     elif event.key == pygame.K_DOWN:
#                         player_action = 2
#                     elif event.key == pygame.K_h:
#                         self.helper_on = not self.helper_on
#                     elif event.key == pygame.K_a:
#                         self.auto_mode = not self.auto_mode
#                 elif event.type == pygame.KEYUP:
#                     if event.key == pygame.K_DOWN:
#                         try:
#                             self.dino.unduck()
#                         except:
#                             pass

#             # helper: compute suggestion (with obstacle type)
#             if self.helper_on:
#                 state = self.get_state()
#                 try:
#                     act = oracle_action(state)
#                 except Exception:
#                     # fallback for older oracle signatures
#                     act = oracle_action(state[:4])
#                 # normalize act
#                 try:
#                     hint_num = int(act)
#                 except:
#                     if isinstance(act, str):
#                         hint_num = 1 if act.lower() == "jump" else (2 if act.lower() == "duck" else 0)
#                     else:
#                         hint_num = 0
#                 self.hint = hint_num
#                 if self.auto_mode:
#                     if hint_num == 1:
#                         self.dino.jump()
#                     elif hint_num == 2:
#                         self.dino.duck()
#             else:
#                 self.hint = None

#             alive = self.step(player_action)

#             # logging
#             state_for_log = self.get_state()
#             oracle_for_log = self.hint if self.hint is not None else -1
#             self.log_step(state_for_log, player_action, oracle_for_log)
#             self.step_idx += 1

#             self.draw()

#             if not alive:
#                 # draw game over message briefly
#                 font = pygame.font.SysFont(None, 36)
#                 surf = font.render(f"Game Over! Final Score: {self.score}", True, BLACK)
#                 self.screen.blit(surf, (WIDTH // 2 - 220, HEIGHT // 2 - 20))
#                 pygame.display.flip()
#                 time.sleep(0.8)
#                 break

#         return self.score

# if __name__ == "__main__":
#     print("# Controls: SPACE=jump, DOWN=duck, H=toggle helper, A=toggle auto-mode")
#     logger = None
#     try:
#         if RunLogger is not None:
#             logger = RunLogger("data/runs/run_human_helper.csv")
#     except Exception:
#         logger = None

#     game = DinoGame(helper_on=True, auto_mode=False, logger=logger)
#     try:
#         while True:
#             s = game.run()
#             print("Run ended, score:", s)
#             try:
#                 if logger:
#                     logger.end_run(s)
#             except:
#                 pass
#             time.sleep(0.2)
#             game.reset()
#     except KeyboardInterrupt:
#         print("Exiting.")
#         if logger:
#             try:
#                 logger.close()
#             except:
#                 pass
#         pygame.quit()

# game.py
import pygame
import random
import time

# optional logger import (if present)
try:
    from logger import RunLogger
except Exception:
    RunLogger = None

from helper import oracle_action

pygame.init()

# Constants
WIDTH, HEIGHT = 960, 360
GROUND_Y = 300
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
FPS = 30

# Dino with jump + duck duration
class Dino:
    def __init__(self):
        self.x = 70
        self.y = GROUND_Y
        self.vel_y = 0
        self.is_jumping = False
        self.is_ducking = False
        self.duck_timer = 0
        self.DUCK_DURATION = int(0.5 * FPS)

    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.vel_y = -13
            self.is_jumping = True

    def duck(self):
        if not self.is_jumping and not self.is_ducking:
            self.is_ducking = True
            self.duck_timer = self.DUCK_DURATION

    def unduck(self):
        self.is_ducking = False
        self.duck_timer = 0

    def update(self):
        # gravity & jump physics
        if self.is_jumping:
            self.y += self.vel_y
            self.vel_y += 0.8
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.is_jumping = False
                self.vel_y = 0
        # duck timer logic
        if self.is_ducking:
            self.duck_timer -= 1
            if self.duck_timer <= 0:
                self.unduck()

    def get_rect(self):
        h = 18 if self.is_ducking else 30
        return pygame.Rect(self.x, self.y - h, 34, h)

    def draw(self, screen):
        r = self.get_rect()
        pygame.draw.rect(screen, (0, 120, 200), r)

# Obstacle with type: 'ground' (on floor) or 'air' (flying)
class Obstacle:
    def __init__(self, x, typ='ground'):
        self.x = x
        self.w = random.choice([18, 22, 26])
        self.type = typ
        
        if typ == 'ground':
            # Ground obstacles - variable heights
            self.h = random.choice([20, 30, 40, 60])
            self.y = GROUND_Y - self.h
        else:  # 'air'
            # FIXED: Air obstacles now spawn LOWER so ducking is useful!
            # Old: y = GROUND_Y - 120 - random(-10,30) = 150-190 (too high!)
            # New: Lower placement so they actually threaten standing dino
            self.h = random.choice([14, 18, 22])
            # Place them at dino head height (standing dino top = 270)
            # Bottom should be around 260-280 to require ducking
            self.y = GROUND_Y - 50 - random.randint(0, 15)  # y = 235-250
            # Bottom will be at 249-272, which hits standing dino (top=270)!
        
        # Color coding
        self.color = (200, 50, 50) if self.type == 'ground' else (150, 50, 200)

    def update(self, speed):
        self.x -= speed

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.get_rect())

# Main game class
class DinoGame:
    def __init__(self, helper_on=True, auto_mode=False, logger=None):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Guided Dino")
        self.clock = pygame.time.Clock()
        self.dino = Dino()
        self.obstacles = []
        self.spawn_timer = 0
        self.speed = 6
        self.score = 0
        self.helper_on = helper_on
        self.auto_mode = auto_mode
        self.hint = None
        self.logger = logger
        self.run_id = int(time.time())
        self.step_idx = 0
        self.high_score = 0

    def reset(self):
        if self.score > self.high_score:
            self.high_score = self.score
        self.dino = Dino()
        self.obstacles = []
        self.spawn_timer = 0
        self.speed = 6
        self.score = 0
        self.hint = None
        self.step_idx = 0

    def spawn_obstacle(self):
        gap = random.randint(160, 360)
        x = WIDTH + gap
        # Increase air obstacle probability for more variety
        typ = 'air' if random.random() < 0.3 else 'ground'
        self.obstacles.append(Obstacle(x, typ=typ))

    def get_nearest(self):
        if not self.obstacles:
            return None
        return min(self.obstacles, key=lambda o: o.x)

    def get_state(self):
        """Returns state with obstacle Y position for better decision making"""
        nearest = self.get_nearest()
        if nearest is None:
            return (9999, 0, self.speed, self.dino.y, self.dino.is_jumping, 'ground', 0)
        d = nearest.x - self.dino.x
        h = nearest.get_rect().height
        obs_y = nearest.y  # ADDED: obstacle Y position
        return (d, h, self.speed, self.dino.y, self.dino.is_jumping, nearest.type, obs_y)

    def step(self, player_action):
        # apply player action
        if player_action == 1:
            self.dino.jump()
        elif player_action == 2:
            self.dino.duck()
        # physics update
        self.dino.update()
        for o in self.obstacles:
            o.update(self.speed)
        self.obstacles = [o for o in self.obstacles if o.x + o.w > -50]

        # spawn logic
        self.spawn_timer += 1
        if self.spawn_timer > int(0.8 * FPS):
            self.spawn_timer = 0
            if random.random() < 0.7:
                self.spawn_obstacle()

        # collision
        dino_rect = self.dino.get_rect()
        for o in self.obstacles:
            if dino_rect.colliderect(o.get_rect()):
                return False

        # scoring & speed ramp
        self.score += 1
        if self.score % 600 == 0:
            self.speed += 1
        return True

    def log_step(self, state, player_action, oracle_action):
        if not self.logger:
            return
        # state for logger: (d,h,speed,y) - keep it simple for compatibility
        try:
            d,h,speed,y,_,_,_ = state
        except:
            try:
                d,h,speed,y,_,_ = state
            except:
                d = state[0]; h = state[1]; speed = state[2]; y = state[3]
        oa = -1 if oracle_action is None else oracle_action
        try:
            oa = int(oa)
        except:
            oa = -1
        try:
            self.logger.log_step((d, h, speed, y), player_action, oa, int(self.helper_on), int(self.score))
        except Exception:
            pass

    def draw_hud(self):
        font = pygame.font.SysFont(None, 22)
        text = f"Score: {self.score}  High: {self.high_score}  Speed: {self.speed}  Helper: {'ON' if self.helper_on else 'OFF'}  Auto: {'ON' if self.auto_mode else 'OFF'}"
        surf = font.render(text, True, BLACK)
        self.screen.blit(surf, (12, 8))

    def draw(self):
        self.screen.fill(WHITE)
        # ground
        pygame.draw.rect(self.screen, GRAY, (0, GROUND_Y + 1, WIDTH, HEIGHT - GROUND_Y))
        # draw dino & obstacles
        self.dino.draw(self.screen)
        for o in self.obstacles:
            o.draw(self.screen)
        # helper hint
        if self.hint is not None and self.helper_on:
            txt = ""
            if self.hint == 1: txt = "JUMP"
            elif self.hint == 2: txt = "DUCK"
            font = pygame.font.SysFont(None, 30)
            surf = font.render(txt, True, (0, 0, 255))
            # show above dino
            self.screen.blit(surf, (self.dino.x + 40, self.dino.y - 60))
        # HUD
        self.draw_hud()
        pygame.display.flip()

    def run(self):
        running = True
        alive = True
        while running and alive:
            self.clock.tick(FPS)
            player_action = 0
            # input handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    alive = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player_action = 1
                    elif event.key == pygame.K_DOWN:
                        player_action = 2
                    elif event.key == pygame.K_h:
                        self.helper_on = not self.helper_on
                    elif event.key == pygame.K_a:
                        self.auto_mode = not self.auto_mode
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        try:
                            self.dino.unduck()
                        except:
                            pass

            # helper: compute suggestion
            if self.helper_on:
                state = self.get_state()
                try:
                    act = oracle_action(state)
                except Exception:
                    # fallback for older oracle signatures
                    try:
                        act = oracle_action(state[:6])
                    except:
                        act = oracle_action(state[:4])
                # normalize act
                try:
                    hint_num = int(act)
                except:
                    if isinstance(act, str):
                        hint_num = 1 if act.lower() == "jump" else (2 if act.lower() == "duck" else 0)
                    else:
                        hint_num = 0
                self.hint = hint_num
                if self.auto_mode:
                    if hint_num == 1:
                        self.dino.jump()
                    elif hint_num == 2:
                        self.dino.duck()
            else:
                self.hint = None

            alive = self.step(player_action)

            # logging
            state_for_log = self.get_state()
            oracle_for_log = self.hint if self.hint is not None else -1
            self.log_step(state_for_log, player_action, oracle_for_log)
            self.step_idx += 1

            self.draw()

            if not alive:
                # draw game over message briefly
                font = pygame.font.SysFont(None, 36)
                surf = font.render(f"Game Over! Final Score: {self.score}", True, BLACK)
                self.screen.blit(surf, (WIDTH // 2 - 220, HEIGHT // 2 - 20))
                pygame.display.flip()
                time.sleep(0.8)
                break

        return self.score

if __name__ == "__main__":
    print("# Controls: SPACE=jump, DOWN=duck, H=toggle helper, A=toggle auto-mode")
    logger = None
    try:
        if RunLogger is not None:
            logger = RunLogger("data/runs/run_human_helper.csv")
    except Exception:
        logger = None

    game = DinoGame(helper_on=True, auto_mode=False, logger=logger)
    try:
        while True:
            s = game.run()
            print("Run ended, score:", s)
            try:
                if logger:
                    logger.end_run(s)
            except:
                pass
            time.sleep(0.2)
            game.reset()
    except KeyboardInterrupt:
        print("Exiting.")
        if logger:
            try:
                logger.close()
            except:
                pass
        pygame.quit()