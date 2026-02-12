from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ._agent import AgentEnum, BaseAgent
from .message import Message, MessageType
from .product import ProductEnum


# Setup Parameters
virgin_stock: int = 10  # inital stock of virgin products
core_stock: int = 0  # inital stock of cores for remanufacturing
reman_stock: int = 0  # inital stock of remanufactured units
delivery_delay: int = 1  # number of days for delivery
manufacture_delay = 5  # Sort of the time it takes to meet the demand (must be >=1 as you cant divide by 0)
remanufacture_delay = 3  # Sort of the time it takes for a core to be collected and turned into a reman product available to buy (must be >=1)
core_acceptance_rate: float = (
    0.7  # Captures the fact that not all cores are usable (cores from reman goods, different amounts of wear on product, etc)
)

if TYPE_CHECKING:
    from .world import World


class OEMStatesEnum(str, Enum):
    OPERATIONAL = "Operational"


class OEM(BaseAgent):
    _state: OEMStatesEnum
    _factory_stock: dict[ProductEnum, float]
    _delivery_delay: int
    _manufacture_delay: int
    _remanufacture_delay: int
    _production_rate: dict[ProductEnum, float]
    _core_stock: float
    _core_acceptance_rate: float

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
        self._manufacture_delay = manufacture_delay
        self._remanufacture_delay = remanufacture_delay
        self._production_rate = {ProductEnum.V: 0, ProductEnum.R: 0}
        self._core_stock = core_stock
        self._core_acceptance_rate = core_acceptance_rate

    def next(self, rng):
        self.update_production()

    def request_product(self, product: ProductEnum) -> bool:
        currentStock = self._factory_stock[product]

        if currentStock >= 1:
            self._factory_stock[product] -= 1
            return True

        return False

    def return_proudct(self, rng) -> None:
        if rng.random() < self._core_acceptance_rate:
            self._core_stock += 1
        else:
            pass

    def update_production(self):
        for product in ProductEnum:
            match product:
                case ProductEnum.V:
                    self._production_rate[product] = (
                        self._world._num_wants[product] + self._world._num_wants_any
                    ) / self._manufacture_delay
                    self._factory_stock[product] += self._production_rate[product]
                    print(
                        f"Production Rate for {product.name}: {self._production_rate[product]:.4f}"
                    )
                    print(
                        f"Factory Stock of {product.name}: {self._factory_stock[product]:.4f}"
                    )
                case ProductEnum.R:
                    desired_production = (
                        self._world._num_wants[product] + self._world._num_wants_any
                    ) / self._remanufacture_delay
                    maximum_production = self._core_stock / self._remanufacture_delay

                    self._production_rate[product] = min(
                        desired_production, maximum_production
                    )

                    self._factory_stock[product] += self._production_rate[product]
                    self._core_stock -= self._production_rate[product]
                    print(f"Core stock: {self._core_stock:.4f}")
                    print(
                        f"Production Rate for {product.name}: {self._production_rate[product]:.4f}"
                    )
                    print(
                        f"Factory Stock of {product.name}: {self._factory_stock[product]:.4f}"
                    )
