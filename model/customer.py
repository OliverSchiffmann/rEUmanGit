from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ._agent import AgentEnum, BaseAgent
from .world import World


advertising_A_effectiveness = (
    0.011  # 1.1% chance of wanting A each day due to advertising
)


class CustomerStatesEnum(str, Enum):
    POTENTIAL_USER = "potential_user"
    WANTS_A = "wants_A"
    USES_A = "uses_A"


class Customer(BaseAgent):
    _state: CustomerStatesEnum

    def __init__(self, id: int, world: World):
        self._state = CustomerStatesEnum.POTENTIAL_USER
        super().__init__(id=id, type=AgentEnum.CUSTOMER, world=world)

    def next(self, rng):
        match self._state:
            case CustomerStatesEnum.POTENTIAL_USER:
                if (
                    rng.random() < advertising_A_effectiveness
                ):  # 1.1% chance of wanting A each day due to advertising
                    self._state = CustomerStatesEnum.WANTS_A
