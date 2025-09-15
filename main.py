from model.customer import Customer
from model.world import World

if __name__ == "__main__":
    world = World()
    customer = Customer(id=0, world=world)
    world.add_agent(customer)
    customer = Customer(id=1, world=world)
    world.add_agent(customer)

    for i in range(0, 30):
        world.tick()
        print(f"World time: {world.now()}")
        print(f"Customers: {world._agents_by_type}")

        world.call_next()
