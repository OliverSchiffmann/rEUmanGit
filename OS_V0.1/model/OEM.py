from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ._agent import AgentEnum, BaseAgent
from .message import Message, MessageType
from .product import ProductEnum


# Setup Parameters
virgin_stock: int = 10
reman_stock: int = 0
delivery_delay: int = 0  # number of days for delivery
manufacture_delay = 5  # Sort of the time it takes to meet the demand (must be >=1 as you cant divide by 0)

if TYPE_CHECKING:
    from .world import World


class OEMStatesEnum(str, Enum):
    OPERATIONAL = "Operational"


class OEM(BaseAgent):
    _state: OEMStatesEnum
    _factory_stock: dict[ProductEnum, float]
    _delivery_delay: int
    _production_rate: dict[ProductEnum, float]

    def __init__(self, id: int, world: World) -> None:
        if manufacture_delay < 1:
            raise ValueError(
                f"manufacture_delay must be >=1. Received: {manufacture_delay}"
            )
        super().__init__(id=id, type=AgentEnum.OEM, world=world)
        self._state = OEMStatesEnum.OPERATIONAL
        self._factory_stock = {
            ProductEnum.V: virgin_stock,
            ProductEnum.R: reman_stock,
        }
        self._delivery_delay = delivery_delay
        self._production_rate = {ProductEnum.V: 0, ProductEnum.R: 0}

    def next(self, rng):
        self.update_production()

    def requestProduct(self, product: ProductEnum) -> bool:
        currentStock = self._factory_stock[product]

        if currentStock >= 1:
            self._factory_stock[product] -= 1
            return True

        return False

    def update_production(self):
        for product in ProductEnum:
            self._production_rate[product] = (
                self._world._num_wants[product] / manufacture_delay
            )
            self._factory_stock[product] += self._production_rate[product]
            print(
                f"Production Rate for {product.name}: {self._production_rate[product]:.4f}"
            )
            print(
                f"Factory Stock of {product.name}: {self._factory_stock[product]:.4f}"
            )
