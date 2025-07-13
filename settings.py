# settings.py
# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Ball settings
BALL_RADIUS = 10
BALL_COLOR = (220, 30, 30)
GRAVITY = 0.1
SPAWN_INTERVAL = 1500  # milliseconds
BALL_INIT_VX_MIN = -2.0
BALL_INIT_VX_MAX =  2.0
COLOR_RANDOM = True

# Bucket settings
BUCKET_WIDTH = 30
BUCKET_HEIGHT = 2
BUCKET_COLOR = (255, 30, 30)
BUCKET_SPEED = 3.5

# Obstacle settings
OBSTACLE_COLOR = (255, 255, 255)
OBSTACLE_RADIUS = 3
    # Number of columns and rows of dots
OBSTACLE_COLUMNS = 6
OBSTACLE_ROWS = 6
    # Where the grid of obstacles starts
OBSTACLE_OFFSET_X = 150
OBSTACLE_OFFSET_Y = 140
    # Spacing between obstacle centers
OBSTACLE_SPACING_X = 100
OBSTACLE_SPACING_Y = 50

# Info panel settings
INFO_PANEL_WIDTH = 200
INFO_PANEL_COLOR = (50, 50, 50)  # dark grey
INFO_TEXT_COLOR = (255, 255, 255)
INFO_FONT_SIZE = 20


# Frames per second
FPS = 60
