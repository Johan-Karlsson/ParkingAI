import numpy as np
import pygame
"""
All constants used in Parking AI are defined here. Note that all
dimensions are given in number of pixels.
"""

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (246, 191, 8)
GREY = (169, 169, 169)

# Game
WINDOW_WIDTH = 200
WINDOW_HEIGHT = 100
FPS = 20
T = 1/FPS

# Car
L = 50
W = int(np.around(L/(212/111)))
Lr = L/2.5
IMAGE = pygame.image.load("car.png")
IMAGE_SCALED = pygame.transform.scale(IMAGE, (L, W))

# Physics
B = 0.8     # Velocity proportional resistance
MIN_VELOCITY = 10

# Parking
HEIGHT = 1.04 * W
WIDTH = 1.04 * L
LINE_WIDTH = 1

# ML
PARKING_REWARD = 100
CRASH_REWARD = -100
