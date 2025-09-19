from enum import Enum
from dataclasses import dataclass


class MessageType(str, Enum):
    BUY_A = "buy_product_a"


@dataclass
class Message:
    sender_id: int
    recipient_id: int
    content: MessageType
