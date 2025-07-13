# game.py

import pygame
import random
from settings import SCREEN_WIDTH, BALL_RADIUS, SCREEN_HEIGHT, SPAWN_INTERVAL, FPS
from ball import Ball
from bucket import Bucket
from obstacles import Obstacles


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Falling Balls and Bucket")
        self.clock = pygame.time.Clock()

        self.bucket = Bucket()
        self.balls = []
        self.obstacles = Obstacles()

        # Set a timer event for spawning balls
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, SPAWN_INTERVAL)

        self.running = True
        self.score = 100

    def spawn_ball(self):
        x = SCREEN_WIDTH / 2
        y = BALL_RADIUS  # just below the top
        self.balls.append(Ball(x, y))

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS)
            self.handle_events()

            self.bucket.update()

            # Update balls
            for ball in list(self.balls):
                ball.update()

                # Bounce off obstacles
                if self.obstacles.check_collision(ball):
                    continue

                # Catch with bucket
                if ball.get_rect().colliderect(self.bucket.get_rect()):
                    self.balls.remove(ball)
                    self.score += 150

                # Remove if off screen
                elif ball.off_screen(SCREEN_HEIGHT):
                    self.balls.remove(ball)

            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.SPAWN_EVENT:
                if(self.score > 9):
                    self.spawn_ball()
                    self.score -= 1.5

    def draw(self):
        self.screen.fill((30, 30, 30))  # background color
        self.obstacles.draw(self.screen)
        self.bucket.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)

        # Draw score
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Dollars: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))

        pygame.display.flip()
