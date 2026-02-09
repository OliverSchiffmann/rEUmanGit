from model.world import World
from model._agent import AgentEnum
from model.customer import Customer, CustomerStatesEnum
from model.product import ProductEnum
from model.OEM import OEM
from numpy import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    rng = random.default_rng(seed=1)
    world = World()

    BtoB_population: int = 100
    simulation_length: int = 365

    results = {
        "day": [],
        "wants_virgin": [],
        "uses_virgin": [],
    }

    oemAgent = OEM(id=-1, world=world)
    world.add_agent(oemAgent)

    for i in range(0, BtoB_population):
        customer = Customer(id=i, world=world, oem=oemAgent)
        world.add_agent(customer)

    for i in range(0, simulation_length):  # model time unit is days bc i said it is
        world.tick()
        print(f"Day {world.now()}")

        print(
            f"Potential users: {world._num_potential_users},\n Wanting Virgin: {world._num_wants[ProductEnum.V]}, Using Virgin: {world._num_uses[ProductEnum.V]}"
        )

        results["day"].append(world.now())
        results["wants_virgin"].append(world._num_wants[ProductEnum.V])
        results["uses_virgin"].append(world._num_uses[ProductEnum.V])

        world.call_next(rng)

    plt.stackplot(
        results["day"],
        results["uses_virgin"],
        results["wants_virgin"],
        labels=["Uses virgin", "Wants virgin"],
    )

    # Add labels and a title for clarity
    plt.title("Customer States Over Time")
    plt.xlabel("Day")
    plt.ylabel("Number of Customers")
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.subplots_adjust(left=0.136, right=0.9, top=0.9, bottom=0.57)
    plt.show()
