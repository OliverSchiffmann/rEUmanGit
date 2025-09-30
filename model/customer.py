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
    WANTS_A = "wants_A"
    USES_A = "uses_A"
    WANTS_B = "wants_B"
    USES_B = "uses_B"
    WANTS_ANY = "wants_any"


product_params = {
    ProductEnum.A: {
        "lifespan": (17, 24),
        "advertising_effectiveness": 0.011,
        "wom_threshold": 0.015,
        "wants_state": CustomerStatesEnum.WANTS_A,
        "uses_state": CustomerStatesEnum.USES_A,
        "buy_message": MessageType.BUY_A,
    },
    ProductEnum.B: {
        "lifespan": (17, 24),
        "advertising_effectiveness": 0.011,
        "wom_threshold": 0.015,
        "wants_state": CustomerStatesEnum.WANTS_B,
        "uses_state": CustomerStatesEnum.USES_B,
        "buy_message": MessageType.BUY_B,
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

    def next(self, rng):
        match self._state:
            case CustomerStatesEnum.POTENTIAL_USER:
                # this section is needed to avoid bias towards one product by always checking that first
                productsToConsider = [ProductEnum.A, ProductEnum.B]
                rng.shuffle(productsToConsider)
                for product in productsToConsider:
                    if (
                        rng.random()
                        < product_params[product]["advertising_effectiveness"]
                    ):  # if a potential user is successfully influenced by ads
                        self.try_and_buy(rng, product)
                        break

            case CustomerStatesEnum.WANTS_A:
                if self._delivery_day != -1:
                    if self._world.now() == self._delivery_day:
                        self.become_user(rng, ProductEnum.A)
                else:
                    if self._world._retailer_stock[ProductEnum.A] >= 1:
                        self._world.confirm_order(ProductEnum.A)
                        if delivery_time == 0:
                            self.become_user(rng, ProductEnum.A)
                        else:
                            self._delivery_day = self._world.now() + delivery_time
                    elif self._world._retailer_stock[ProductEnum.A] < 1:
                        if (
                            self._end_of_patience_day != -1
                            and self._world.now() == self._end_of_patience_day
                        ):
                            self._state = CustomerStatesEnum.WANTS_ANY
                            self._end_of_patience_day = -1
                            self._active_product = None

            case CustomerStatesEnum.WANTS_B:
                if self._delivery_day != -1:
                    if self._world.now() == self._delivery_day:
                        self.become_user(rng, ProductEnum.B)
                else:
                    if self._world._retailer_stock[ProductEnum.B] >= 1:
                        self._world.confirm_order(ProductEnum.B)
                        if delivery_time == 0:
                            self.become_user(rng, ProductEnum.B)
                        else:
                            self._delivery_day = self._world.now() + delivery_time
                    elif self._world._retailer_stock[ProductEnum.B] < 1:
                        if (
                            self._end_of_patience_day != -1
                            and self._world.now() == self._end_of_patience_day
                        ):
                            self._state = CustomerStatesEnum.WANTS_ANY
                            self._end_of_patience_day = -1
                            self._active_product = None

            case CustomerStatesEnum.WANTS_ANY:
                if self._active_product != None:
                    if self._world.now() == self._delivery_day:
                        self.become_user(rng, self._active_product)
                else:
                    productsToConsider = [ProductEnum.A, ProductEnum.B]
                    rng.shuffle(productsToConsider)
                    for product in productsToConsider:
                        if self._world._retailer_stock[product] >= 1:
                            self._world.confirm_order(product)
                            if delivery_time == 0:
                                self.become_user(rng, product)
                            else:
                                self._active_product = product
                                self._delivery_day = self._world.now() + delivery_time
                            break

            case CustomerStatesEnum.USES_A:
                if self._world.now() == self._end_of_life_day:
                    self._state = product_params[ProductEnum.A]["wants_state"]
                    self._end_of_life_day = -1
                else:
                    for _ in range(contact_per_day):
                        if (
                            rng.random()
                            < product_params[ProductEnum.A]["wom_threshold"]
                        ):
                            recipient_id = self._world.get_random_agent_id(
                                exclude_id=self._id
                            )
                            if (
                                recipient_id != -1
                            ):  # checks if there is someone to send to
                                message = Message(
                                    sender_id=self._id,
                                    recipient_id=recipient_id,
                                    content=MessageType.BUY_A,
                                )
                                self._world.recieve_message(message)

            case CustomerStatesEnum.USES_B:
                if self._world.now() == self._end_of_life_day:
                    self._state = product_params[ProductEnum.B]["wants_state"]
                    self._end_of_life_day = -1
                else:
                    for _ in range(contact_per_day):
                        if (
                            rng.random()
                            < product_params[ProductEnum.B]["wom_threshold"]
                        ):
                            recipient_id = self._world.get_random_agent_id(
                                exclude_id=self._id
                            )
                            if (
                                recipient_id != -1
                            ):  # checks if there is someone to send to
                                message = Message(
                                    sender_id=self._id,
                                    recipient_id=recipient_id,
                                    content=MessageType.BUY_B,
                                )
                                self._world.recieve_message(message)

    def try_and_buy(self, rng, product: ProductEnum):
        if self._world._retailer_stock[product] >= 1:
            self._world.confirm_order(product)
            if delivery_time == 0:  # checking if delivery is instant
                self.become_user(rng, product)
            else:
                self._state = product_params[product]["wants_state"]
                self._active_product = product
                self._delivery_day = self._world.now() + delivery_time
        else:
            self._state = product_params[product]["wants_state"]
            self._active_product = product
            self._end_of_patience_day = self._world.now() + patience

    def become_user(self, rng, product: ProductEnum):
        self._state = product_params[product]["uses_state"]
        self._active_product = product
        self._delivery_day = -1
        self._end_of_patience_day = -1

        lifespan_range = product_params[product]["lifespan"]
        lifespan = rng.integers(*lifespan_range)
        self._end_of_life_day = self._world.now() + lifespan

    def state(self):
        return self._state

    def handle_message(self, message: Message, rng):
        if (
            self._state == CustomerStatesEnum.POTENTIAL_USER
            and message.content == MessageType.BUY_A
        ):
            self.try_and_buy(rng, ProductEnum.A)
        elif (
            self._state == CustomerStatesEnum.POTENTIAL_USER
            and message.content == MessageType.BUY_B
        ):
            self.try_and_buy(rng, ProductEnum.B)
