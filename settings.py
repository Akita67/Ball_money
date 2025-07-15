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
BUCKET_HEIGHT = 1
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

# A list of colors for the halo effect
HALO_COLORS = [
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
]


# Info panel settings
INFO_PANEL_WIDTH = 120
INFO_PANEL_COLOR = (30, 30, 30)  # A slightly darker grey
INFO_TEXT_COLOR = (200, 200, 200) # A bit softer than pure white
INFO_FONT_SIZE = 20 # a smaller font size
INFO_PANEL_BORDER_COLOR = (255, 215, 0)  # Gold color for the border
INFO_PANEL_TITLE_COLOR = (255, 255, 255) # White for the title


# Frames per second
FPS = 60