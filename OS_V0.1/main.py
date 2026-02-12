from model.world import World
from model._agent import AgentEnum
from model.customer import Customer, CustomerStatesEnum
from model.product import ProductEnum
from model.OEM import OEM
from numpy import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    rng = random.default_rng(seed=1)
    world = World(enable_reman=True)  # Toggle reman on/off with True/False

    BtoB_population: int = 100
    simulation_length: int = 1200  # number of DAYS the simulation runs for

    results = {
        "day": [],
        "potential_users": [],
        "wants_virgin": [],
        "uses_virgin": [],
        "wants_reman": [],
        "uses_reman": [],
        "wants_any": [],
        "core_stock": [],
        "virgin_stock": [],
        "reman_stock": [],
    }

    oemAgent = OEM(id=-1, world=world)
    world.add_agent(oemAgent)

    for i in range(0, BtoB_population):
        customer = Customer(id=i, world=world, oem=oemAgent)
        world.add_agent(customer)

    for i in range(0, simulation_length):  # model time unit is days bc i said it is
        world.tick()
        print(f"---------")
        print(f"Day {world.now()}:\n")

        print(
            f"Potential users: {world._num_potential_users},\n Wanting Virgin: {world._num_wants[ProductEnum.V]}, Using Virgin: {world._num_uses[ProductEnum.V]}\n Wanting Reman: {world._num_wants[ProductEnum.R]}, Using Reman: {world._num_uses[ProductEnum.R]}\n"
        )

        results["day"].append(world.now())
        results["potential_users"].append(world._num_potential_users)
        results["wants_virgin"].append(world._num_wants[ProductEnum.V])
        results["uses_virgin"].append(world._num_uses[ProductEnum.V])
        results["wants_reman"].append(world._num_wants[ProductEnum.R])
        results["uses_reman"].append(world._num_uses[ProductEnum.R])
        results["wants_any"].append(world._num_wants_any)
        results["core_stock"].append(oemAgent._core_stock)
        results["virgin_stock"].append(oemAgent._factory_stock[ProductEnum.V])
        results["reman_stock"].append(oemAgent._factory_stock[ProductEnum.R])

        world.call_next(rng)

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(10, 8))

    colours = [
        "#2fa8e9",  # Potential Users (Light Blue)
        "#fb9a99",  # Wants Virgin (Light Red)
        "#d91c1f",  # Uses Virgin (Dark Red)
        "#bce499",  # Wants Reman (Light Green)
        "#33a02c",  # Uses Reman (Dark Green)
        "#D1AB23",  # Wants any
    ]

    ax1.stackplot(
        results["day"],
        results["potential_users"],
        results["wants_virgin"],
        results["uses_virgin"],
        results["wants_reman"],
        results["uses_reman"],
        results["wants_any"],
        labels=[
            "Potential Users",
            "Wants virgin",
            "Uses virgin",
            "Wants reman",
            "Uses reman",
            "Wants any",
        ],
        colors=colours,
    )

    ax1.set_title("Customer States Over Time")
    ax1.set_ylabel("Number of Customers")
    ax1.legend(loc="lower left")
    ax1.grid(True, alpha=0.3)

    ax2.plot(
        results["day"],
        results["core_stock"],
        color="#807E7E",
        linewidth=2,
        label="Core Stock",
    )
    ax2.plot(
        results["day"],
        results["virgin_stock"],
        color="#d91c1f",
        linewidth=2,
        label="Virgin Stock",
    )
    ax2.plot(
        results["day"],
        results["reman_stock"],
        color="#33a02c",
        linewidth=2,
        label="Reman Stock",
    )

    ax2.set_title("OEM Inventory Level")
    ax2.set_xlabel("Day")
    ax2.set_ylabel("Units")
    ax2.legend(loc="upper left")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
