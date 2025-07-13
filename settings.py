# settings.py
# Window dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750

# Ball settings
BALL_RADIUS = 7
BALL_COLOR = (255, 250, 250)
GRAVITY = 0.1
SPAWN_INTERVAL = 1500  # milliseconds
BALL_INIT_VX_MIN = -2.0
BALL_INIT_VX_MAX =  2.0
COLOR_RANDOM = True

# Bucket settings
BUCKET_WIDTH = 43
BUCKET_HEIGHT = 3
BUCKET_COLOR = (50, 100, 255)
BUCKET_SPEED = 3.5

# Obstacle settings
OBSTACLE_COLOR = (255, 255, 255)
OBSTACLE_RADIUS = 8
    # Number of columns and rows of dots
OBSTACLE_COLUMNS = 10
OBSTACLE_ROWS = 5
    # Where the grid of obstacles starts
OBSTACLE_OFFSET_X = 120
OBSTACLE_OFFSET_Y = 140
    # Spacing between obstacle centers
OBSTACLE_SPACING_X = 100
OBSTACLE_SPACING_Y = 80

# Frames per second
FPS = 60
