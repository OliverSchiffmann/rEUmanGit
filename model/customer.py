from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from ._agent import AgentEnum, BaseAgent
from .world import World


class JobStatesEnum(str, Enum):
    POTENTIAL_USER = "potential_user"


class Customer(BaseAgent):
    _state: JobStatesEnum

    def __init__(self, id: int, world: World):
        self._state = JobStatesEnum.POTENTIAL_USER
        super().__init__(
            id=id, type=AgentEnum.CUSTOMER, world=world
        )  # not sure what is going on here exactly
