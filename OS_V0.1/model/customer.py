from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ._agent import AgentEnum, BaseAgent
from .message import Message, MessageType
from .product import ProductEnum


delivery_time: int = 0  # days
contact_per_day: int = 5  # number of people a user contacts each day
patience: int = 2  # number of days a customer will wait for delivery before giving up


if TYPE_CHECKING:
    from .world import World


class CustomerStatesEnum(str, Enum):
    POTENTIAL_USER = "potential_user"


product_params = {
    ProductEnum.V: {
        "lifespan": (17, 24),
        "advertising_effectiveness": 0.011,
        "wom_threshold": 0.015,
    },
    ProductEnum.R: {
        "lifespan": (17, 24),
        "advertising_effectiveness": 0.011,
        "wom_threshold": 0.015,
    },
}


class Customer(BaseAgent):
    _state: CustomerStatesEnum
    _delivery_day: int
    _end_of_life_day: int
    _end_of_patience_day: int
    _active_product: ProductEnum | None

    def __init__(self, id: int, world: World):
        self._state = CustomerStatesEnum.POTENTIAL_USER
        self._delivery_day = -1
        self._end_of_life_day = -1
        self._end_of_patience_day = -1
        self._active_product = None
        super().__init__(id=id, type=AgentEnum.CUSTOMER, world=world)
