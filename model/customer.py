from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ._agent import AgentEnum, BaseAgent


advertising_A_effectiveness = (
    0.011  # 1.1% chance of wanting A each day due to advertising
)
delivery_time: int = 0  # days

if TYPE_CHECKING:
    from .world import World


class CustomerStatesEnum(str, Enum):
    POTENTIAL_USER = "potential_user"
    WANTS_A = "wants_A"
    USES_A = "uses_A"


class Customer(BaseAgent):
    _state: CustomerStatesEnum
    _delivery_day: int

    def __init__(self, id: int, world: World):
        self._state = CustomerStatesEnum.POTENTIAL_USER
        self._delivery_day = -1
        super().__init__(id=id, type=AgentEnum.CUSTOMER, world=world)

    def next(self, rng, day: int, retailer_stock: float):
        match self._state:
            case CustomerStatesEnum.POTENTIAL_USER:
                if (
                    rng.random() < advertising_A_effectiveness
                ):  # if a potential user is successfully influenced by ads
                    if retailer_stock >= 1:
                        self._world.confirm_order()
                        if delivery_time == 0:  # checking if delivery is instant
                            self.become_user_A()
                        else:
                            self._state = CustomerStatesEnum.WANTS_A
                            self._delivery_day = day + delivery_time
                    else:
                        self._state = CustomerStatesEnum.WANTS_A

            case CustomerStatesEnum.WANTS_A:
                if self._delivery_day != -1:
                    if day == self._delivery_day:
                        self._state = CustomerStatesEnum.USES_A
                else:
                    if retailer_stock >= 1:
                        self._world.confirm_order()
                        if delivery_time == 0:
                            self.become_user_A()
                        else:
                            self._delivery_day = day + delivery_time

    def become_user_A(self):
        self._state = CustomerStatesEnum.USES_A
        self._delivery_day = -1

    def state(self):
        return self._state
