from __future__ import annotations
from collections import Counter
from typing import TYPE_CHECKING
from model._agent import AgentEnum, BaseAgent
from . import customer


inital_retailer_stock_A: int = 100
inital_factory_stock_A: int = 0
delivery_delay: int = (
    2  # number of days for delivery from factory to retailer (must be >=1)
)

if TYPE_CHECKING:
    from .customer import Customer, CustomerStatesEnum


class World:
    _now: int
    _agents: dict[int, BaseAgent]
    _agents_by_type: dict[AgentEnum, list[int]]
    _retailer_stock_A: float
    _factory_stock_A: float
    _production_rate_A: float
    _num_potential_users: int
    _num_wants_A: int
    _num_uses_A: int

    def __init__(self) -> None:
        self._now = 0
        self._agents = {}
        self._agents_by_type = {AgentEnum.CUSTOMER: []}
        self._retailer_stock_A = inital_retailer_stock_A
        self._factory_stock_A = inital_factory_stock_A
        self._production_rate_A = 0
        self._num_potential_users = 0
        self._num_wants_A = 0
        self._num_uses_A = 0

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
        self.update_production_A()
        self.deliver_to_retailer_A()
        for _, agent in self._agents.items():
            agent.next(rng, self._now, self._retailer_stock_A)

    def update_customer_state_counts(self):
        customer_states = [
            agent.state()
            for agent in self._agents.values()
            if isinstance(agent, customer.Customer)
        ]
        counts = Counter(customer_states)
        from .customer import CustomerStatesEnum

        self._num_potential_users = counts.get(CustomerStatesEnum.POTENTIAL_USER, 0)
        self._num_wants_A = counts.get(CustomerStatesEnum.WANTS_A, 0)
        self._num_uses_A = counts.get(CustomerStatesEnum.USES_A, 0)

    def update_production_A(self):
        self._production_rate_A = self._num_wants_A
        print(f"Production Rate for A: {self._production_rate_A}")
        self._factory_stock_A += self._production_rate_A
        print(f"Factory Stock of A: {self._factory_stock_A:.4f}")

    def deliver_to_retailer_A(self):
        units_delivered = self._factory_stock_A / delivery_delay
        print(f"Units delivered from Factory: {units_delivered:.4f}")
        self._retailer_stock_A += units_delivered
        self._factory_stock_A -= units_delivered
        print(f"Retailer Stock of A: {self._retailer_stock_A:.4f}")

    def confirm_order(self):
        self._retailer_stock_A = self._retailer_stock_A - 1
