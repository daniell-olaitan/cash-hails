from pydantic import BaseModel
from utils import (
    TransactionStatus,
    TransactionType
)


class UserSchema(BaseModel):
    phone: str
    username: str
    password: str


class AdminSchema(BaseModel):
    phone: str
    username: str
    password: str
    bank_name: str = None
    bank_account_name: str = None
    bank_account_number: str = None


class WalletSchema(BaseModel):
    balance: int


class TransactionSchema(BaseModel):
    amount: int
    bank_transaction_id: str
    type: TransactionType
    status: TransactionStatus


class OrderSchema(BaseModel):
    serving_progress: int
    daily_return_time: str = None


class ProductSchema(BaseModel):
    name: str
    price: int
    duration: int
    daily_income: int
