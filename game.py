# game.py
import pygame
import random
from helper import oracle_action

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 300
GROUND_Y = 250
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)

# Dino class
class Dino:
    def __init__(self):
        self.x = 50
        self.y = GROUND_Y
        self.vel_y = 0
        self.is_jumping = False
        self.is_ducking = False

    def jump(self):
        if not self.is_jumping:
            self.vel_y = -10
            self.is_jumping = True

    def duck(self):
        self.is_ducking = True

    def unduck(self):
        self.is_ducking = False

    def update(self):
        if self.is_jumping:
            self.y += self.vel_y
            self.vel_y += 0.5
            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.is_jumping = False

    def draw(self, screen):
        color = (0, 100, 200)
        rect = pygame.Rect(self.x, self.y - (30 if not self.is_ducking else 10), 30, 30)
        pygame.draw.rect(screen, color, rect)

# Obstacle class
class Obstacle:
    def __init__(self, x):
        self.x = x
        self.h = random.choice([30, 50, 70])
        self.w = 20

    def update(self, speed):
        self.x -= speed

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 50, 50), (self.x, GROUND_Y - self.h, self.w, self.h))

# Main game
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Guided Dino Game")

    clock = pygame.time.Clock()
    dino = Dino()
    obstacles = [Obstacle(600)]
    running = True
    helper_on = True
    speed = 6
    score = 0

    while running:
        clock.tick(30)
        screen.fill(WHITE)
        pygame.draw.line(screen, GRAY, (0, GROUND_Y + 1), (WIDTH, GROUND_Y + 1), 2)

        # Spawn obstacles
        if len(obstacles) == 0 or obstacles[-1].x < 400:
            obstacles.append(Obstacle(WIDTH + random.randint(100, 300)))

        # Game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
                elif event.key == pygame.K_DOWN:
                    dino.duck()
                elif event.key == pygame.K_h:
                    helper_on = not helper_on
                    print("Helper:", helper_on)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.unduck()

        # Update
        dino.update()
        for obs in obstacles:
            obs.update(speed)
        obstacles = [o for o in obstacles if o.x + o.w > 0]

        # AI Helper suggestion
        if helper_on and obstacles:
            obs = obstacles[0]
            state = (obs.x - dino.x, obs.h, speed, dino.y)
            act = oracle_action(state)
            if act == "jump":
                dino.jump()
            elif act == "duck":
                dino.duck()
            else:
                dino.unduck()

        # Collision detection
        for obs in obstacles:
            if obs.x < dino.x + 30 and obs.x + obs.w > dino.x and dino.y > GROUND_Y - obs.h:
                print("Game Over! Final Score:", score)
                running = False

        # Draw
        dino.draw(screen)
        for obs in obstacles:
            obs.draw(screen)

        score += 1
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    print("# Controls: SPACE=jump, DOWN=duck, H=toggle helper")
    main()
