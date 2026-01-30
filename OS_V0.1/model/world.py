from __future__ import annotations
from typing import TYPE_CHECKING
from model._agent import AgentEnum, BaseAgent
import random
from .message import Message
from .product import ProductEnum


virgin_stock: int = 100
reman_stock: int = 0

delivery_delay: int = 2  # number of days for delivery (must be >=1)

if TYPE_CHECKING:
    from .customer import Customer, CustomerStatesEnum


class World:
    _now: int
    _agents: dict[int, BaseAgent]
    _agents_by_type: dict[AgentEnum, list[int]]
    _retailer_stock: dict[ProductEnum, float]

    def __init__(self) -> None:
        self._now = 0
        self._agents = {}
        self._agents_by_type = {AgentEnum.CUSTOMER: []}
        self._retailer_stock = {
            ProductEnum.V: virgin_stock,
            ProductEnum.R: reman_stock,
        }

    def tick(self) -> None:
        self._now += 1

    def now(self) -> int:
        return self._now

    def add_agent(self, agent: BaseAgent):
        if agent.id() in self._agents:
            exit(f"Agent with id already exists. Received: {agent.id}")
        self._agents[agent.id()] = agent
        self._agents_by_type[agent.type()].append(agent.id())
