from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from ._agent import AgentEnum, BaseAgent
from .message import Message, MessageType


advertising_A_effectiveness = 0.011  # % chance of wanting A each day due to advertising
delivery_time: int = 0  # days
contact_per_day: int = 5  # number of people a user contacts each day
word_of_mouth_threshold: float = (
    0.015  # models 5 daily interactions with a % chance of convincing
)
expected_lifespan_A: tuple = (17, 24)  # days (inc, excl)


if TYPE_CHECKING:
    from .world import World


class CustomerStatesEnum(str, Enum):
    POTENTIAL_USER = "potential_user"
    WANTS_A = "wants_A"
    USES_A = "uses_A"


class Customer(BaseAgent):
    _state: CustomerStatesEnum
    _delivery_day: int
    _end_of_life_A: int

    def __init__(self, id: int, world: World):
        self._state = CustomerStatesEnum.POTENTIAL_USER
        self._delivery_day = -1
        self._end_of_life_A = -1
        super().__init__(id=id, type=AgentEnum.CUSTOMER, world=world)

    def next(self, rng):
        match self._state:
            case CustomerStatesEnum.POTENTIAL_USER:
                if (
                    rng.random() < advertising_A_effectiveness
                ):  # if a potential user is successfully influenced by ads
                    self.try_and_buy_A(rng)

            case CustomerStatesEnum.WANTS_A:
                if self._delivery_day != -1:
                    if self._world.now() == self._delivery_day:
                        self.become_user_A(rng)
                else:
                    if self._world._retailer_stock_A >= 1:
                        self._world.confirm_order()
                        if delivery_time == 0:
                            self.become_user_A(rng)
                        else:
                            self._delivery_day = self._world.now() + delivery_time

            case CustomerStatesEnum.USES_A:
                if self._world.now() == self._end_of_life_A:
                    self._state = CustomerStatesEnum.WANTS_A
                    self._end_of_life_A = -1
                else:
                    for _ in range(contact_per_day):
                        if rng.random() < word_of_mouth_threshold:
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

    def try_and_buy_A(self, rng):
        if self._world._retailer_stock_A >= 1:
            self._world.confirm_order()
            if delivery_time == 0:  # checking if delivery is instant
                self.become_user_A(rng)
            else:
                self._state = CustomerStatesEnum.WANTS_A
                self._delivery_day = self._world.now() + delivery_time
        else:
            self._state = CustomerStatesEnum.WANTS_A

    def become_user_A(self, rng):
        self._state = CustomerStatesEnum.USES_A
        self._delivery_day = -1
        lifespan_A = rng.integers(*expected_lifespan_A)
        self._end_of_life_A = self._world.now() + lifespan_A

    def state(self):
        return self._state

    def handle_message(self, message: Message, rng):
        if (
            self._state == CustomerStatesEnum.POTENTIAL_USER
            and message.content == MessageType.BUY_A
        ):
            self.try_and_buy_A(rng)
