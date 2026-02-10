from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ._agent import AgentEnum, BaseAgent
from .message import Message, MessageType
from .product import ProductEnum


contact_per_day: int = 5  # number of people a user contacts each day


if TYPE_CHECKING:
    from .world import World
    from .OEM import OEM


class CustomerStatesEnum(str, Enum):
    POTENTIAL_USER = "potential_user"
    WANTS_VIRGIN = "wants_virgin"
    USES_VIRGIN = "uses_virgin"


product_params = {
    ProductEnum.V: {
        "lifespan": (
            17,
            24,
        ),  # number of days that a product might last for when in use
        "advertising_effectiveness": 0.011,
        "wom_threshold": 0.015,
        "wants_state": CustomerStatesEnum.WANTS_VIRGIN,
        "uses_state": CustomerStatesEnum.USES_VIRGIN,
        "buy_message": MessageType.BUY_V,
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
    _active_product: ProductEnum | None
    _oem: OEM

    def __init__(self, id: int, world: World, oem: OEM):
        self._state = CustomerStatesEnum.POTENTIAL_USER
        self._delivery_day = -1
        self._end_of_life_day = -1
        self._active_product = None
        super().__init__(id=id, type=AgentEnum.CUSTOMER, world=world)
        self._oem = oem

    def next(self, rng):
        match self._state:
            case CustomerStatesEnum.POTENTIAL_USER:
                # this section is needed to avoid bias towards one product by always checking that first
                productsToConsider = self._world.get_active_products()
                rng.shuffle(productsToConsider)
                for product in productsToConsider:
                    if (
                        rng.random()
                        < product_params[product]["advertising_effectiveness"]
                    ):  # if a potential user is successfully influenced by ads
                        self.try_and_buy(rng, product)
                        break
            case CustomerStatesEnum.WANTS_VIRGIN:
                if self._delivery_day != -1:
                    if self._world.now() == self._delivery_day:
                        self.become_user(rng, ProductEnum.V)
                else:
                    if (
                        self._active_product is not None
                    ):  # should be ProductEnum.V as the only way to get into the state is through try and buy but it wants a guarantee
                        self.try_and_buy(rng, self._active_product)
                    else:
                        self.try_and_buy(rng, ProductEnum.V)

            case CustomerStatesEnum.USES_VIRGIN:
                if self._world.now() == self._end_of_life_day:
                    self._state = product_params[ProductEnum.V]["wants_state"]
                    self._end_of_life_day = -1

    def try_and_buy(self, rng, product: ProductEnum):
        purchaseSuccessful = self._oem.requestProduct(product)

        if purchaseSuccessful:
            if self._oem._delivery_delay == 0:  # checking if delivery is instant
                self.become_user(rng, product)
            else:
                self._state = product_params[product]["wants_state"]
                self._active_product = product
                self._delivery_day = self._world.now() + self._oem._delivery_delay
        else:
            self._state = product_params[product]["wants_state"]
            self._active_product = product
            # To Do: add logic that increases the manufacturing rate (actually should just be in the OEM agent base don number of customers in wants_virgin state)

    def become_user(self, rng, product: ProductEnum):
        self._state = product_params[product]["uses_state"]
        self._active_product = product
        self._delivery_day = -1

        lifespan_range = product_params[product]["lifespan"]
        lifespan = rng.integers(*lifespan_range)
        self._end_of_life_day = self._world.now() + lifespan
