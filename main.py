import pygame
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
        self.image_org = pygame.image.load("car.png")  # add .convert() to speed up
        # self.image.set_colorkey(const.BLACK)
        self.v = 0
        self.a = 0
        self.theta = 0
        self.theta_change = 0
        self.L = 212
        self.Lr = self.L/2
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
            self.delta = -np.pi/9
        elif pressed_keys[pygame.K_RIGHT]:
            self.delta = np.pi/9
        if pressed_keys[pygame.K_UP]:
            self.a = 100
        elif pressed_keys[pygame.K_DOWN]:
            self.a = -100
    
    def rotate(self):
        theta_deg = - np.rad2deg(self.theta)
        self.image = pygame.transform.rotate(self.image_org, theta_deg)
        self.rect = self.image.get_rect(center=self.rect_org.center)

    def update(self):
        self.beta = np.arctan(self.Lr*np.tan(self.delta)/self.L)
        self.v += self.a * const.T
        self.theta_change = self.v*np.tan(self.delta)*np.cos(self.beta)/self.L
        self.theta += self.theta_change * const.T
        self.theta = self.theta % (2*np.pi)
        self.x_change = self.v * np.cos(self.beta + self.theta)
        self.y_change = self.v * np.sin(self.beta + self.theta)
        self.x += self.x_change * const.T
        self.y += self.y_change * const.T
        self.rotate()
        self.rect.center = (self.x, self.y)

        print("Vel: ", self.v)
        print("Theta: ", self.theta)
        print("Delta: ", self.delta)
        
        self.a = 0
        self.delta = 0


# %%
pygame.init()
screen = pygame.display.set_mode((1200, 720))
pygame.display.set_caption('Parking AI')
clock = pygame.time.Clock()
all_sprites = pygame.sprite.Group()
crashed = False
car = Car(600, 360)
all_sprites.add(car)

font = pygame.font.Font(pygame.font.get_default_font(), 18)

while not crashed:
    clock.tick(const.FPS)
    events = pygame.event.get()
    crashed = car.control(events)
    all_sprites.update()
    screen.fill(const.WHITE)
    text_surface = font.render("Vel: {}  Theta: {}  Delta: {} Change: {}".format(
        car.v, car.theta_change, car.delta, (int(car.x_change), int(car.y_change))),
         True, pygame.Color('orange'))
    screen.blit(text_surface, dest=(0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
quit()
