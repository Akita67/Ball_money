import time
import pygame
import sys
import random

# Import settings and game components
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS, SPAWN_INTERVAL, FPS, UI_BACKGROUND_COLOR, BALL_COST, MULTIPLIER
from ball import Ball
from bucket import Bucket
from obstacles import Obstacles
from info_panel import InfoPanel
from screenrecorder import ScreenRecorder
from effects import Particle, FloatingText


class Game:
    def __init__(self):
        pygame.init()
        self.window_title = "Falling Balls and Bucket"
        pygame.display.set_caption(self.window_title)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Game objects
        self.bucket = Bucket()
        self.balls = []
        self.obstacles = Obstacles()
        self.info_panel = InfoPanel()
        self.score = 14.0
        self.cost_per_ball = BALL_COST
        self.multiplier = MULTIPLIER
        self.running = True

        # Visual effects
        self.particles = []
        self.floating_texts = []
        self.score_font = pygame.font.SysFont("Impact", 30)

        # Timers
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, SPAWN_INTERVAL)

        # Screen Recorder
        self.recorder = ScreenRecorder(
            SCREEN_WIDTH, SCREEN_HEIGHT, FPS, self.window_title
        )
        pygame.time.delay(500)
        self.recorder.start()

    def spawn_ball(self):
        x = SCREEN_WIDTH / 2
        y = BALL_RADIUS
        self.balls.append(Ball(x, y))

    def trigger_score_effect(self, x, y):
        for _ in range(random.randint(20, 30)):
            self.particles.append(Particle(x, y))
        self.floating_texts.append(FloatingText(x, y, f"+{MULTIPLIER*BALL_COST}", self.score_font))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.SPAWN_EVENT and self.score >= self.cost_per_ball and pygame.time.get_ticks() // 1000 < 61:
                self.spawn_ball()
                self.score -= self.cost_per_ball
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the start button was clicked
                if self.info_panel.is_start_button_clicked(event.pos):
                    print("Start Autobet button clicked!")
                    # Here you can add the logic to start/stop auto-betting
                    self.spawn_ball() # For now, let's just spawn one ball


    def update(self, dt):
        self.bucket.update()
        self.obstacles.update_bucket_walls(self.bucket.get_wall_rects())

        for ball in list(self.balls):
            ball.update()
            self.obstacles.check_collision(ball)
            if ball.get_rect().colliderect(self.bucket.get_rect()):
                self.trigger_score_effect(ball.x, ball.y)
                self.balls.remove(ball)
                self.score += MULTIPLIER*BALL_COST
            elif ball.off_screen(SCREEN_HEIGHT):
                self.balls.remove(ball)

        for p in list(self.particles):
            p.update()
            if p.lifespan <= 0: self.particles.remove(p)
        for t in list(self.floating_texts):
            t.update()
            if t.lifespan <= 0: self.floating_texts.remove(t)

    def draw(self):
        self.screen.fill(UI_BACKGROUND_COLOR)

        self.obstacles.draw(self.screen)
        self.bucket.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)
        for p in self.particles: p.draw(self.screen)
        for t in self.floating_texts: t.draw(self.screen)

        # Draw the new info panel with the current game data
        self.info_panel.draw(
            surface=self.screen,
            score=self.score,
            balls=len(self.balls),
            time=pygame.time.get_ticks() // 1000,
            cost=self.cost_per_ball,
            multiplier=self.multiplier
        )

        pygame.display.flip()

    def run(self):
        try:
            while self.running:
                dt = self.clock.tick(FPS)
                self.handle_events()
                self.update(dt)
                self.draw()
                if (self.score <= self.cost_per_ball and not self.balls) or (pygame.time.get_ticks() // 1000 > 61 and not self.balls):
                    self.running = False
        finally:
            time.sleep(1)
            self.recorder.stop()
            pygame.quit()
            print("Game exited cleanly.")
            sys.exit()