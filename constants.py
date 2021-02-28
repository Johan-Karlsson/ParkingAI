"""
All constants used in Parking AI are defined here. Note that all
dimensions are given in number of pixels.
"""

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (246, 191, 8)
GREY = (169,169,169)

# Game
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 720
FPS = 30
T = 1/FPS

# Car
L = 212
Lr = L/2.5

# Physics
B = 0.8     # Velocity proportional resistance
MIN_VELOCITY = 10

# Parking
HEIGHT = 120
WIDTH = 220
LINE_WIDTH = 4

# ML
PARKING_REWARD = 100
CRASH_REWARD = -100