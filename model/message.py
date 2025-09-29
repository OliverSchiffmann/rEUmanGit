from enum import Enum
from dataclasses import dataclass


class MessageType(str, Enum):
    BUY_A = "buy_product_a"
    BUY_B = "buy_product_b"


@dataclass
class Message:
    sender_id: int
    recipient_id: int
    content: MessageType
