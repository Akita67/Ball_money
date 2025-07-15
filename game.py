import time
import pygame
import sys
import random

# Import settings and game components from other files
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS, SPAWN_INTERVAL, FPS
from ball import Ball
from bucket import Bucket
from obstacles import Obstacles
from info_panel import InfoPanel
from screenrecorder import ScreenRecorder
# --- NEW: Import the effect classes from effects.py ---
from effects import Particle, FloatingText


class Game:
    """
    The main class that runs the game loop, handles events,
    updates game state, and draws to the screen.
    """

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
        self.score = 10  # Start with some score for testing
        self.running = True

        # --- NEW: Lists to hold active visual effects ---
        self.particles = []
        self.floating_texts = []
        self.score_font = pygame.font.SysFont("Impact", 30)


        # Timer for spawning new balls
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, SPAWN_INTERVAL)

        # Initialize the screen recorder
        self.recorder = ScreenRecorder(
            SCREEN_WIDTH, SCREEN_HEIGHT, FPS, self.window_title
        )
        pygame.time.delay(500)
        self.recorder.start()

    def spawn_ball(self):
        """Creates a new ball at the top-center of the screen."""
        x = SCREEN_WIDTH / 2
        y = BALL_RADIUS
        self.balls.append(Ball(x, y))

    # --- NEW: Method to create all score effects at once ---
    def trigger_score_effect(self, x, y):
        """Creates particles and floating text when a ball is scored."""
        # Create a burst of 20-30 particles
        for _ in range(random.randint(20, 30)):
            self.particles.append(Particle(x, y))
        # Create the floating "+250" text
        self.floating_texts.append(FloatingText(x, y, "+250", self.score_font))
        # You could also add a sound effect here, e.g.:
        # self.score_sound.play()

    def handle_events(self):
        """Processes all pygame events, such as quitting or timers."""
        min_cost = 2.5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.SPAWN_EVENT and self.score >= min_cost and pygame.time.get_ticks()//1000 < 61:
                self.spawn_ball()
                self.score -= min_cost

    def update(self, dt):
        """Updates the state of all game objects."""
        self.bucket.update()
        walls = self.bucket.get_wall_rects()
        self.obstacles.update_bucket_walls(walls)

        for ball in list(self.balls):
            ball.update()
            if self.obstacles.check_collision(ball):
                continue

            # --- UPDATED: Collision with bucket now triggers the effect ---
            if ball.get_rect().colliderect(self.bucket.get_rect()):
                self.trigger_score_effect(ball.x, ball.y) # Trigger effect at ball's location
                self.balls.remove(ball)
                self.score += 250
            elif ball.off_screen(SCREEN_HEIGHT):
                self.balls.remove(ball)

        # --- NEW: Update all active particles and floating texts ---
        for particle in list(self.particles):
            particle.update()
            if particle.lifespan <= 0:
                self.particles.remove(particle)

        for text in list(self.floating_texts):
            text.update()
            if text.lifespan <= 0:
                self.floating_texts.remove(text)


    def draw(self):
        """Draws all game objects to the screen."""
        self.screen.fill((30, 30, 30))

        self.obstacles.draw(self.screen)
        self.bucket.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)

        # --- NEW: Draw all the visual effects ---
        for particle in self.particles:
            particle.draw(self.screen)
        for text in self.floating_texts:
            text.draw(self.screen)

        self.info_panel.update_info([
            "",
            "",
            "",
            f"SOLD: {self.score:.1f}",
            "",
            f"BALLS: {len(self.balls)}",
            "",
            f"TIME: {pygame.time.get_ticks() // 1000}s",
            "",
            f"COST: {2.5}$",
            "",
            f"MULTI: 100"
        ])
        self.info_panel.draw(self.screen)

        pygame.display.flip()

    def run(self):
        """The main game loop."""
        try:
            while self.running:
                dt = self.clock.tick(FPS)
                self.handle_events()
                self.update(dt)
                self.draw()
                # Stop if score is too low OR if time is up
                if (self.score <= 0 and not self.balls) or (pygame.time.get_ticks() // 1000 > 61 and not self.balls):
                    self.running = False
        finally:
            time.sleep(1)
            self.recorder.stop()
            pygame.quit()
            print("Game exited cleanly.")
            sys.exit()