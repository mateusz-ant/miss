import simpy

from hare import Hare


env = simpy.Environment()
hare = Hare(env)
env.run(until=25)