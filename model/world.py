from __future__ import annotations
from collections import Counter
from typing import TYPE_CHECKING
from model._agent import AgentEnum, BaseAgent
import random
from .message import Message
from . import customer
from .product import ProductEnum


inital_retailer_stock_A: int = 100
inital_retailer_stock_B: int = 100
inital_factory_stock_A: int = 0
inital_factory_stock_B: int = 0

delivery_delay: int = (
    2  # number of days for delivery from factory to retailer (must be >=1)
)

if TYPE_CHECKING:
    from .customer import Customer, CustomerStatesEnum


class World:
    _now: int
    _agents: dict[int, BaseAgent]
    _agents_by_type: dict[AgentEnum, list[int]]
    _retailer_stock: dict[ProductEnum, float]
    _factory_stock: dict[ProductEnum, float]
    _production_rate: dict[ProductEnum, float]
    _num_potential_users: int
    _num_wants_any: int
    _num_wants: dict[ProductEnum, int]
    _num_uses: dict[ProductEnum, int]
    _message_queue: list[Message]

    def __init__(self) -> None:
        self._now = 0
        self._agents = {}
        self._agents_by_type = {AgentEnum.CUSTOMER: []}
        self._retailer_stock = {
            ProductEnum.A: inital_retailer_stock_A,
            ProductEnum.B: inital_retailer_stock_B,
        }
        self._factory_stock = {
            ProductEnum.A: inital_factory_stock_A,
            ProductEnum.B: inital_factory_stock_B,
        }
        self._production_rate = {ProductEnum.A: 0, ProductEnum.B: 0}
        self._num_potential_users = 0
        self._num_wants_any = 0
        self._num_wants = {ProductEnum.A: 0, ProductEnum.B: 0}
        self._num_uses = {ProductEnum.A: 0, ProductEnum.B: 0}
        self._message_queue = []

    def tick(self) -> None:
        self._now += 1
        self.update_customer_state_counts()

    def now(self) -> int:
        return self._now

    def add_agent(self, agent: BaseAgent):
        if agent.id() in self._agents:
            exit(f"Agent with id already exists. Received: {agent.id}")
        self._agents[agent.id()] = agent
        self._agents_by_type[agent.type()].append(agent.id())

    def call_next(self, rng):
        self.update_production()
        self.deliver_to_retailer()
        for _, agent in self._agents.items():
            agent.next(rng)
        self.process_messages(rng)

    def update_customer_state_counts(self):
        from .customer import CustomerStatesEnum

        self._num_wants = {product: 0 for product in ProductEnum}
        self._num_uses = {product: 0 for product in ProductEnum}
        potential_users = 0
        users_wanting_any = 0

        for agent in self._agents.values():
            if isinstance(agent, customer.Customer):
                if agent.state() == CustomerStatesEnum.POTENTIAL_USER:
                    potential_users += 1
                elif agent.state() == CustomerStatesEnum.WANTS_A:
                    self._num_wants[ProductEnum.A] += 1
                elif agent.state() == CustomerStatesEnum.WANTS_B:
                    self._num_wants[ProductEnum.B] += 1
                elif agent.state() == CustomerStatesEnum.USES_A:
                    self._num_uses[ProductEnum.A] += 1
                elif agent.state() == CustomerStatesEnum.USES_B:
                    self._num_uses[ProductEnum.B] += 1
                elif agent.state() == CustomerStatesEnum.WANTS_ANY:
                    users_wanting_any += 1
        self._num_potential_users = potential_users
        self._num_wants_any = users_wanting_any

    def update_production(self):
        for product in ProductEnum:
            self._production_rate[product] = (
                self._num_wants[product] + self._num_wants_any
            )
            self._factory_stock[product] += self._production_rate[product]
            print(
                f"Production Rate for {product.name}: {self._production_rate[product]}"
            )
            print(
                f"Factory Stock of {product.name}: {self._factory_stock[product]:.4f}"
            )

    def deliver_to_retailer(self):
        for product in ProductEnum:
            units_delivered = self._factory_stock[product] / delivery_delay
            self._retailer_stock[product] += units_delivered
            self._factory_stock[product] -= units_delivered
            print(
                f"Units of {product.name} delivered from Factory: {units_delivered:.4f}"
            )
            print(
                f"Retailer Stock of {product.name}: {self._retailer_stock[product]:.4f}"
            )

    def confirm_order(self, product: ProductEnum):
        self._retailer_stock[product] = self._retailer_stock[product] - 1

    def recieve_message(self, message: Message):
        self._message_queue.append(message)

    def get_random_agent_id(self, exclude_id: int) -> int:
        agent_ids = [id for id in self._agents.keys() if id != exclude_id]
        if not agent_ids:
            return -1  # No other agents to send to
        return random.choice(agent_ids)

    def process_messages(self, rng):
        for message in self._message_queue:
            recipient = self._agents.get(message.recipient_id)
            if recipient:
                recipient.handle_message(message, rng)
        self._message_queue.clear()
