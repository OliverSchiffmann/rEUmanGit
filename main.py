from model.world import World
from model._agent import AgentEnum
from model.customer import Customer, CustomerStatesEnum
from numpy import random

if __name__ == "__main__":
    rng = random.default_rng(seed=1)
    world = World()

    customer_population = 1000

    for i in range(0, customer_population):
        customer = Customer(id=i, world=world)
        world.add_agent(customer)

    for i in range(0, 365):  # model time unit is days bc i said it is
        world.tick()
        print(f"Day {world.now()}")
        print(
            f"Customers: {world._agents_by_type[AgentEnum.CUSTOMER][:5]}...{world._agents_by_type[AgentEnum.CUSTOMER][-5:]}"
        )

        potential_user_count = 0
        wants_A_count = 0
        uses_A_count = 0
        for agent in world._agents.values():
            if (
                agent._state == CustomerStatesEnum.POTENTIAL_USER
            ):  # confused about issues accessig _state
                potential_user_count += 1
            elif agent._state == CustomerStatesEnum.WANTS_A:
                wants_A_count += 1
            elif agent._state == CustomerStatesEnum.USES_A:
                uses_A_count += 1
        print(
            f"Potential users: {potential_user_count}, Wanting A: {wants_A_count}, Using A: {uses_A_count}"
        )

        world.call_next(rng)
