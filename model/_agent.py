from __future__ import annotations

from enum import Enum

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # IDK what this does
    from .world import World


class AgentEnum(str, Enum):  # what does that mean 'enumeration'?
    CUSTOMER = "customer"


class BaseAgent:
    _world: World
    _id: int
    _type: AgentEnum

    def __init__(self, world: World, id: int, type: AgentEnum):
        self._world = world
        self._id = id
        self._type = type

    def id(self) -> int:
        return self._id

    def type(self) -> AgentEnum:
        return self._type

    def next(self):
        return
