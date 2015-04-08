import random
import simpy
import pygame

from models.meadow import Meadow

ENV_RUNNING_TIME = 100
SCREEN_LENGTH = 800
SCREEN_HEIGHT = 600
class Main:

    def __init__(self):
        self.env = simpy.Environment()
        self.meadow = Meadow(self.env)
        self.env.run(until=ENV_RUNNING_TIME)
        self.running = True
        self.display = None

    def init_pygame(self):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_LENGTH,SCREEN_HEIGHT))
        pygame.display.set_caption('Wolf Hare Coevoultion Simulation')

    def simulation(self):
        self.init_pygame()
        self.start_rendering()

    def start_rendering(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                print(event)

            for hare in self.meadow.hares:
                x = random.random() * SCREEN_LENGTH
                y = random.random() * SCREEN_HEIGHT
                hare.show_up(self.display, x, y)

            for wolf in self.meadow.wolves:
                x = random.random() * SCREEN_LENGTH
                y = random.random() * SCREEN_HEIGHT
                wolf.show_up(self.display, x, y)

            pygame.display.update()
            clock.tick(60)
        self.stop_rendering()

    def stop_rendering(self):
        pygame.quit()


if __name__ == "__main__":
    main = Main()
    main.simulation()