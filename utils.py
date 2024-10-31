from enum import Enum
from datetime import datetime


def generate_id(prefix: str) -> str:
    return prefix + datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]


class TransactionStatus(Enum):
    FAIL = 0
    SUCCESS = 1
    PENDING = 2


class TransactionType(Enum):
    WITHDRAWAL = 0
    DEPOSIT = 1
    PURCHASE = 2
