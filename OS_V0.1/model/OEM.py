from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ._agent import AgentEnum, BaseAgent
from .message import Message, MessageType
from .product import ProductEnum


# Setup Parameters
virgin_stock: int = 100
reman_stock: int = 0
delivery_delay: int = 2  # number of days for delivery (must be >=1)

if TYPE_CHECKING:
    from .world import World


class OEMStatesEnum(str, Enum):
    OPERATIONAL = "Operational"


class OEM(BaseAgent):
    _state: OEMStatesEnum
    _retailer_stock: dict[ProductEnum, float]

    def __init__(self, id: int, world: World) -> None:
        super().__init__(id=id, type=AgentEnum.OEM, world=world)
        self._state = OEMStatesEnum.OPERATIONAL
        self._retailer_stock = {
            ProductEnum.V: virgin_stock,
            ProductEnum.R: reman_stock,
        }

    def requestProduct(self, product: ProductEnum) -> bool:
        currentStock = self._retailer_stock[product]

        if currentStock >= 1:
            self._retailer_stock[product] -= 1
            return True

        return False
