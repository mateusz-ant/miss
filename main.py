import random
import simpy
import pygame

from models.meadow import Meadow
from parameters import *


class Main:
    def __init__(self):
        self.env = None
        self.meadow = None
        self.running = True
        self.display = None

    def init_env(self):
        self.env = simpy.Environment()
        self.meadow = Meadow(self.env, self.display)
        self.env.run(until=ENV_RUNNING_TIME)

    def init_pygame(self):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Wolf Hare Coevoultion Simulation')

    def stop_rendering(self):
        pygame.quit()

    def simulation(self):
        self.init_pygame()
        self.init_env()
        self.start_rendering()

    def start_rendering(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                print(event)
            pygame.display.update()
            clock.tick(60)
        self.stop_rendering()


if __name__ == "__main__":
    main = Main()
    main.simulation()