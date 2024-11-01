from enum import Enum
from datetime import datetime


def generate_id(prefix: str) -> str:
    return prefix + datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]


class TransactionStatus(Enum):
    FAIL = 'failed'
    SUCCESS = 'successful'
    PENDING = 'pending'


class TransactionType(Enum):
    WITHDRAWAL = 'withdrawal'
    DEPOSIT = 'deposit'
    PURCHASE = 'purchase'
