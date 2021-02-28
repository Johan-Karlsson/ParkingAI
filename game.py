import pygame
from pygame.locals import *
import constants as const
import numpy as np
from classes import Car, Parking
import argparse

# %%
def print_states(screen, font, car):
    v = int(car.v)
    delta = np.round(car.delta, 2)
    theta = np.round(car.theta, 2)

    text_surface = font.render("Vel: {}  Delta: {}  Theta: {}"
                               .format(v, delta, theta), True, const.YELLOW)
    screen.blit(text_surface, dest=(0, 0))

# %%
def get_reward(car, parking, crashed, parked) -> float:
    if crashed:
        print("Crash!")
        return const.CRASH_REWARD
    elif parked:
        print("Parked!")
        return const.PARKING_REWARD
    else:
       dist = np.sqrt((car.x - parking.x_center)**2 + (car.y - parking.y_center)**2)
       return 1/dist

# %%
def main(car_pos: tuple, parking_pos: tuple) -> float:
    """
    Given intitial position and parking position, this function
    runs the game environment.
    """
    pygame.init()
    screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
    pygame.display.set_caption('Parking AI')
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    crashed, closed, parked = False, False, False
    # Create car instance and add to list of sprites
    car = Car(car_pos)
    all_sprites.add(car)
    # Create parking instance and add to list of sprites
    parking = Parking(parking_pos)

    font = pygame.font.Font(pygame.font.get_default_font(), 18)

    scores = []
    while not (crashed or closed or parked):
        clock.tick(const.FPS)
        events = pygame.event.get()
        closed = car.control(events)
        all_sprites.update()
        # Check car status and calculate score
        crashed = car.check_boundary_crash(screen)
        parked = parking.car_is_parked(car)
        score = get_reward(car, parking, crashed, parked)
        scores.append(score)
        # Update graphics
        screen.fill(const.GREY)
        print_states(screen, font, car)
        parking.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    return sum(scores)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the parking game environment")
    parser.add_argument("--car_pos", "-cp", type=int, nargs=2, help="Car start position",
                        default=(const.WINDOW_WIDTH/2, const.WINDOW_HEIGHT/2))
    parser.add_argument("--parking_pos", "-pp", type=int, nargs=2, help="Parking position",
                        default=(const.WINDOW_WIDTH/2*1.5, const.WINDOW_HEIGHT/2))
    args = parser.parse_args()
    score = main(tuple(args.car_pos), tuple(args.parking_pos))
    print("Score:", score)
