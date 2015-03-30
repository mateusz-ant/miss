import simpy

from models.meadow import Meadow

ENV_RUNNING_TIME = 50

def main():

    env = simpy.Environment()
    meadow = Meadow(env)
    env.run(until=ENV_RUNNING_TIME)

if __name__ == "__main__":
    main()