import time

import pygame
import sys

# Import settings and game components from other files
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS, SPAWN_INTERVAL, FPS
from ball import Ball
from bucket import Bucket
from obstacles import Obstacles
from info_panel import InfoPanel
from screenrecorder import ScreenRecorder


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
        self.score = 2.5  # Start with some score for testing
        self.running = True

        # Timer for spawning new balls
        self.SPAWN_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_EVENT, SPAWN_INTERVAL)

        # Initialize the screen recorder
        # Use 'nvenc' for NVIDIA GPUs (recommended) or 'cpu' as a fallback.
        self.recorder = ScreenRecorder(
            SCREEN_WIDTH, SCREEN_HEIGHT, FPS, self.window_title,
            output_file="game_recording.mp4",
            encoder="nvenc"
        )
        # A small delay to ensure the window is fully rendered before recording starts
        pygame.time.delay(500)
        self.recorder.start()

    def spawn_ball(self):
        """Creates a new ball at the top-center of the screen."""
        x = SCREEN_WIDTH / 2
        y = BALL_RADIUS
        self.balls.append(Ball(x, y))

    def handle_events(self):
        """Processes all pygame events, such as quitting or timers."""
        min_cost = 2.5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == self.SPAWN_EVENT and self.score >= min_cost:
                self.spawn_ball()
                self.score -= min_cost

    def update(self, dt):
        """Updates the state of all game objects."""
        self.bucket.update()
        walls = self.bucket.get_wall_rects()
        self.obstacles.update_bucket_walls(walls)

        # Iterate over a copy of the list to safely remove items
        for ball in list(self.balls):
            ball.update()  # Note: Your original ball.py doesn't use dt, but it's good practice

            # Check for collisions with obstacles
            if self.obstacles.check_collision(ball):
                continue  # Collision handled in the method

            # Check for collision with the bucket (scoring)
            if ball.get_rect().colliderect(self.bucket.get_rect()):
                self.balls.remove(ball)
                self.score += 250
            # Check if the ball has gone off-screen
            elif ball.off_screen(SCREEN_HEIGHT):
                self.balls.remove(ball)

    def draw(self):
        """Draws all game objects to the screen."""
        self.screen.fill((30, 30, 30))  # Dark grey background

        # Draw game elements
        self.obstacles.draw(self.screen)
        self.bucket.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)

        # Update and draw the info panel
        self.info_panel.update_info([
            f"Balance: {self.score:.1f}",
            f"Balls: {len(self.balls)}",
            f"Time: {pygame.time.get_ticks() // 1000}s",
            f"Ball Cost: {2.5}$",
            f"Multiplier: {"X"}100"

            #f"FPS: {self.clock.get_fps():.1f}",
            #f"Encoder: {self.recorder.encoder.upper()}"
        ])
        self.info_panel.draw(self.screen)

        # Update the full display
        pygame.display.flip()

    def run(self):
        """The main game loop."""
        try:
            while self.running:
                # dt is the time in milliseconds since the last frame
                dt = self.clock.tick(FPS)
                self.handle_events()
                self.update(dt)
                self.draw()
                # End condition
                if self.score <= 0 and not self.balls:
                    self.running = False
        finally:
            # Ensure everything shuts down cleanly
            time.sleep(1)
            self.recorder.stop()
            pygame.quit()
            print("Game exited cleanly.")
            sys.exit()
