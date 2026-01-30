from model.world import World
from model._agent import AgentEnum
from model.customer import Customer, CustomerStatesEnum
from model.product import ProductEnum
from numpy import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    rng = random.default_rng(seed=1)
    world = World()

    BtoB_population: int = 100
    simulation_length: int = 365

    results = {
        "day": [],
    }

    for i in range(0, BtoB_population):
        customer = Customer(id=i, world=world)
        world.add_agent(customer)

    for i in range(0, simulation_length):  # model time unit is days bc i said it is
        world.tick()
        print(f"Day {world.now()}")
