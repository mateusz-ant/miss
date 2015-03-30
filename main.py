import simpy

from hare import Hare
from wolf import Wolf


def main():
    ENV_RUNNING_TIME = 500
    NUM_OF_HARES = 10
    NUM_OF_WOLVES = 3

    env = simpy.Environment()
    wolves = [Wolf(env, name="wolf_" + str(x)) for x in range(NUM_OF_WOLVES)]
    hares = [Hare(env, name="hare_" + str(x)) for x in range(NUM_OF_HARES)]

    hare = Hare(env)
    env.run(until=ENV_RUNNING_TIME)

if __name__ == "__main__":
    main()