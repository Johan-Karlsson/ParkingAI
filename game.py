import pygame
from pygame.locals import * # noqa
import constants as const
import numpy as np
from classes import Car, Parking
import argparse


# %%
def print_states(screen, car):
    v = int(car.v)
    delta = np.round(car.delta, 2)
    theta = np.round(car.theta, 2)
    font = pygame.font.Font(pygame.font.get_default_font(), 18)
    text_surface = font.render("Vel: {}  Delta: {}  Theta: {}"
                               .format(v, delta, theta), True, const.YELLOW)
    screen.blit(text_surface, dest=(0, 0))


# %%
def get_reward(car, parking, crashed, parked):
    if crashed:
        print("Crash!")
        return const.CRASH_REWARD
    elif parked:
        print("Parked!")
        return const.PARKING_REWARD
    else:
        prev_parking_distance = car.parking_distance
        new_parking_distance = car.update_parking_distance(parking)
        if new_parking_distance < prev_parking_distance:
            return 1
        elif new_parking_distance > prev_parking_distance:
            return -1
        else:
            return 0


# %%
def main(ai_control: bool, car_pos: tuple, parking_pos: tuple) -> float:
    """
    Given intitial car and parking positions, this function
    runs the game environment.
    """
    pygame.init()
    screen = pygame.display.set_mode((const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
    pygame.display.set_caption('Parking AI')
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    crashed, closed, parked = False, False, False
    # Create car instance and add to list of sprites
    car = Car(car_pos, ai_control)
    all_sprites.add(car)
    # Create parking instance and check distance from car
    parking = Parking(parking_pos)
    car.update_parking_distance(parking)

    scores = []
    pixels = []
    while not (crashed or closed or parked):
        clock.tick(const.FPS)
        events = pygame.event.get()
        pixels.append(pygame.surfarray.array2d(screen))
        closed = car.control(events, pixels[-1])
        all_sprites.update()
        # Check car status and calculate score
        crashed = car.check_boundary_crash(screen)
        parked = parking.car_is_parked(car)
        score = get_reward(car, parking, crashed, parked)
        scores.append(score)
        # Update graphics
        screen.fill(const.GREY)
        # print_states(screen, car)
        parking.draw(screen)
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    return scores, pixels


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the parking game")
    parser.add_argument("--ai_control", "-ai", action='store_true',
                        default=False, help="Give car control to AI")
    parser.add_argument("--car_pos", "-cp", type=int,
                        nargs=2, help="Car start position",
                        default=(const.WINDOW_WIDTH/2, const.WINDOW_HEIGHT/2))
    parser.add_argument("--parking_pos", "-pp", type=int,
                        nargs=2, help="Parking position",
                        default=(200, 300))
    args = parser.parse_args()
    car_pos = tuple(args.car_pos)
    parking_pos = tuple(args.parking_pos)
    scores, pixels = main(args.ai_control, car_pos, parking_pos)
    print("Scores:", scores)
