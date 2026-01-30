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


class OEM:
    _retailer_stock: dict[ProductEnum, float]

    def __init__(self) -> None:
        self._retailer_stock = {
            ProductEnum.V: virgin_stock,
            ProductEnum.R: reman_stock,
        }
