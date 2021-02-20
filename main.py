import pygame
from pygame.locals import *
import constants as const
import numpy as np


# %%
class Car(pygame.sprite.Sprite):
    """
    Bicycle model from:
    https://dingyan89.medium.com/simple-understanding-of-kinematic-bicycle-model-81cac6420357
    """
    def __init__(self, x_start, y_start):
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
        self.x, self.y = (x_start, y_start)
        self.rect.center = (x_start, y_start)
        self.rotate()

    def control(self, events):
        # Check for events
        for event in events:
            if event.type == pygame.QUIT:
                return True

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

    def rotate(self):
        theta_deg = - np.rad2deg(self.theta)
        self.image = pygame.transform.rotate(self.image_org, theta_deg)
        self.rect = self.image.get_rect(center=self.rect_org.center)

    def update(self):
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


# %%
class Parking:
    def __init__(self, x_center, y_center):
        x = x_center - const.WIDTH/2
        y = y_center - const.HEIGHT/2
        self.rect = pygame.Rect(x, y, const.WIDTH, const.HEIGHT)
        self.color = const.WHITE
        self.line_width = const.LINE_WIDTH
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, self.line_width)



# %%
def print_states(screen, font, car):
    v = int(car.v)
    delta = np.round(car.delta, 2)
    theta = np.round(car.theta, 2)

    text_surface = font.render("Vel: {}  Delta: {}  Theta: {}"
                               .format(v, delta, theta), True, const.YELLOW)
    screen.blit(text_surface, dest=(0, 0))


# %%
pygame.init()
screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption('Parking AI')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
crashed = False
# Create car instance and add to list of sprites
car = Car(600, 360)
all_sprites.add(car)
# Create parking instance and add to list of sprites
parking = Parking(600, 360)
all_sprites.add(car)

font = pygame.font.Font(pygame.font.get_default_font(), 18)

while not crashed:
    clock.tick(const.FPS)
    events = pygame.event.get()
    crashed = car.control(events)
    all_sprites.update()
    screen.fill(const.GREY)
    print_states(screen, font, car)
    parking.draw(screen)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
quit()
