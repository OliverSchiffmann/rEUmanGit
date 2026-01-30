from model.world import World
from model._agent import AgentEnum
from model.customer import Customer, CustomerStatesEnum
from model.product import ProductEnum
from numpy import random
import matplotlib.pyplot as plt

if __name__ == "__main__":
    rng = random.default_rng(seed=1)
    world = World()

    customer_population: int = 1000
    simulation_length: int = 180

    results = {
        "day": [],
        "wants_A": [],
        "uses_A": [],
        "wants_B": [],
        "uses_B": [],
        "wants_any": [],
    }

    for i in range(0, customer_population):
        customer = Customer(id=i, world=world)
        world.add_agent(customer)

    for i in range(0, simulation_length):  # model time unit is days bc i said it is
        world.tick()
        print(f"Day {world.now()}")
        print(
            f"Customers: {world._agents_by_type[AgentEnum.CUSTOMER][:5]}...{world._agents_by_type[AgentEnum.CUSTOMER][-5:]}"
        )

        print(
            f"Potential users: {world._num_potential_users},\n Wanting A: {world._num_wants[ProductEnum.A]}, Using A: {world._num_uses[ProductEnum.A]},\n Wanting B: {world._num_wants[ProductEnum.B]}, Using B: {world._num_uses[ProductEnum.B], }\n Wanting Any: {world._num_wants_any}"
        )

        results["day"].append(world.now())
        results["wants_A"].append(world._num_wants[ProductEnum.A])
        results["uses_A"].append(world._num_uses[ProductEnum.A])
        results["wants_B"].append(world._num_wants[ProductEnum.B])
        results["uses_B"].append(world._num_uses[ProductEnum.B])
        results["wants_any"].append(world._num_wants_any)

        world.call_next(rng)

    plt.stackplot(
        results["day"],
        results["uses_A"],
        results["wants_A"],
        results["uses_B"],
        results["wants_B"],
        results["wants_any"],
        labels=["Uses A", "Wants A", "Uses B", "Wants B", "Wants Any"],
    )

    # Add labels and a title for clarity
    plt.title("Customer States Over Time")
    plt.xlabel("Day")
    plt.ylabel("Number of Customers")
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.subplots_adjust(left=0.136, right=0.9, top=0.9, bottom=0.57)
    plt.show()
