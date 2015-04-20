import random

ENV_RUNNING_TIME = 100000
SCREEN_LENGTH = 800
SCREEN_HEIGHT = 600

REPORT_INTERVAL = 5
NUM_OF_HARES = 6
NUM_OF_WOLVES = 3


def rand_x():
    return random.random() * SCREEN_LENGTH


def rand_y():
    return random.random() * SCREEN_HEIGHT