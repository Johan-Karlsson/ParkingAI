import pygame
from pygame.locals import * # noqa
import constants as const
import numpy as np
from tensorflow.keras import layers, models
import time


# %% Car class
class Car(pygame.sprite.Sprite):
    """
    Bicycle model from:
    https://dingyan89.medium.com/simple-understanding-of-kinematic-bicycle-model-81cac6420357
    """
    def __init__(self, start_pos, ai_control):
        pygame.sprite.Sprite.__init__(self)
        self.image_org = pygame.image.load("car.png")  # .convert() to speed up
        # self.image.set_colorkey(const.BLACK)
        self.v = 0
        self.a = 0
        self.theta = 0
        self.theta_change = 0
        self.L = const.L
        self.Lr = const.Lr
        self.delta = 0
        self.beta = np.arctan(self.Lr*np.tan(self.delta)/self.L)
        self.image = self.image_org
        self.rect_org = self.image_org.get_rect()
        self.rect = self.image.get_rect()
        self.x, self.y = start_pos
        self.rect.center = start_pos
        self.rotate()
        self.parking_distance = None
        self.shortest_parking_distance = 1e6
        self.ai_control = ai_control
        if ai_control:
            self.agent = Agent()
        else:
            self.agent = None

    def control(self, events, pixels):
        # Check for events
        for event in events:
            if event.type == pygame.QUIT:
                return True

        if not self.ai_control:
            self.manual_control()
        else:
            self.ai_action(pixels)

    def rotate(self):
        theta_deg = - np.rad2deg(self.theta)
        self.image = pygame.transform.rotate(self.image_org, theta_deg)
        self.rect = self.image.get_rect(center=self.rect_org.center)

    def update(self):

        # If the velocity is very low, set it to zero
        if np.abs(self.v) < const.MIN_VELOCITY and self.a == 0:
            self.v = 0

        self.beta = np.arctan(self.Lr*np.tan(self.delta)/self.L)
        self.v += (self.a - const.B * self.v) * const.T
        self.theta_change = self.v*np.tan(self.delta)*np.cos(self.beta)/self.L
        self.theta += self.theta_change * const.T
        self.theta = self.theta % (2*np.pi)
        self.x_change = self.v * np.cos(self.beta + self.theta)
        self.y_change = self.v * np.sin(self.beta + self.theta)
        self.x += self.x_change * const.T
        self.y += self.y_change * const.T
        self.rotate()
        self.rect.center = (self.x, self.y)

    def check_boundary_crash(self, screen) -> bool:
        screen_rect = screen.get_rect()
        return not screen_rect.contains(self.rect)

    def update_parking_distance(self, parking) -> float:
        x_dist = self.x - parking.x_center
        y_dist = self.y - parking.y_center
        self.parking_distance = np.sqrt(x_dist**2 + y_dist**2)
        if self.parking_distance < self.shortest_parking_distance:
            self.shortest_parking_distance = self.parking_distance
        return self.parking_distance

    def manual_control(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.delta = -np.pi/5
        elif pressed_keys[pygame.K_RIGHT]:
            self.delta = np.pi/5
        else:
            self.delta = 0
        if pressed_keys[pygame.K_UP]:
            self.a = 100
        elif pressed_keys[pygame.K_DOWN]:
            self.a = -100
        else:
            self.a = 0

    def ai_action(self, pixels):
        action = self.agent.control(pixels)
        if action[0] > 0.5:
            self.delta = -np.pi/5
        elif action[1] > 0.5:
            self.delta = np.pi/5
        else:
            self.delta = 0
        if action[2] > 0.5:
            self.a = 100
        elif action[3] > 0.5:
            self.a = -100
        else:
            self.a = 0
        return action


# %% Parking class
class Parking:
    def __init__(self, pos):
        x, y = pos
        self.x_center = x
        self.y_center = y
        x -= const.WIDTH/2
        y -= const.HEIGHT/2
        self.rect = pygame.Rect(x, y, const.WIDTH, const.HEIGHT)
        self.color = const.WHITE
        self.line_width = const.LINE_WIDTH

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.line_width)

    def car_is_parked(self, car) -> bool:
        return self.rect.contains(car.rect)


# %% Agent class
class Agent:
    def __init__(self):
        self.model = self.build()

    def build(self):
        model = models.Sequential()
        model.add(layers.Conv2D(16, (8, 8), activation='relu',
                  input_shape=(const.WINDOW_WIDTH, const.WINDOW_HEIGHT, 1)))
        model.add(layers.Flatten())
        model.add(layers.Dense(4, activation='sigmoid'))
        model.compile(optimizer='adam')
        return model

    def control(self, pixels) -> int:
        data = pixels.reshape(1, 480, 480, 1)
        start = time.time()
        action = self.model.predict(data)[0]
        stop = time.time()
        action_time = stop - start
        print("Action: {} Time: {}".format(action, action_time))
        return action
