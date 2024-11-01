from functools import wraps
from typing import (
    Dict,
    Type,
    Tuple,
    Callable
)
from flask import request
from pydantic import BaseModel
from models.utils import (
    TransactionStatus,
    TransactionType
)


class UserRegSchema(BaseModel):
    phone: str
    username: str
    password: str

    class Config:
        extra = "forbid"


class LoginSchema(BaseModel):
    phone: str
    password: str

    class Config:
        extra = "forbid"


class AdminRegSchema(BaseModel):
    phone: str
    username: str
    password: str
    bank_name: str = None
    bank_account_name: str = None
    bank_account_number: str = None

    class Config:
        extra = "forbid"


class ChangePwdSchema(BaseModel):
    current_password: str
    new_password: str
    confirm_password: str = None

    class Config:
        extra = "forbid"


class WalletSchema(BaseModel):
    balance: int

    class Config:
        extra = "forbid"


class TransactionSchema(BaseModel):
    amount: int
    bank_transaction_id: str
    type: TransactionType
    status: TransactionStatus

    class Config:
        extra = "forbid"


class OrderSchema(BaseModel):
    serving_progress: int
    daily_return_time: str = None

    class Config:
        extra = "forbid"


class ProductSchema(BaseModel):
    name: str
    price: int
    duration: int
    daily_income: int

    class Config:
        extra = "forbid"


def validate_input(schema_type: Type[BaseModel], **input: Dict) -> bool:
    try:
        return bool(schema_type(**input))
    except ValueError as err:
        print(err)
        return False


def verify_json_input(f: Callable) -> Callable:
    from exc import AbortException

    @wraps(f)
    def wrapper(*args: Tuple, **kwargs: Dict) -> Callable:
        if not request.is_json:
            raise AbortException({'error': f"wrong format: {request.content_type}"})

        return f(*args, **kwargs)
    return wrapper
