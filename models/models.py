from models import db
from utils import (
    generate_id,
    TransactionStatus,
    TransactionType
)
from models.parent_models import ParentModel
from typing import Dict


class User(ParentModel, db.Model):
    __tablename__ = 'users'
    phone = db.Column(db.String(16), nullable=False, unique=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Admin(User, db.Model):
    __tablename__ = 'admins'
    bank_name = db.Column(db.String(60))
    bank_account_name = db.Column(db.String(128))
    bank_account_number = db.Column(db.String(10), unique=True)


class Wallet(ParentModel, db.Model):
    __tablename__ = 'wallets'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    balance = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Numeric(precision=20, scale=2), nullable=False, default=0)


class Order(ParentModel, db.Model):
    __tablename__ = 'orders'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(60), db.ForeignKey('products.id'), nullable=False)
    order_id = db.Column(db.String(20), nullable=False, default=generate_id('OR'))
    serving_progress = db.Column(db.Integer, nullable=False, default=0)
    daily_return_time = db.Column(db.String(20))


class Product(ParentModel, db.Model):
    __tablename__ = 'products'
    name = db.Column(db.String(128), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(precision=20, scale=2), nullable=False)
    daily_income = db.Column(db.Numeric(precision=20, scale=2), nullable=False)


class Transaction(ParentModel, db.Model):
    __tablename__ = 'transactions'
    wallet_id = db.Column(db.String(60), db.ForeignKey('wallets.id'))
    admin_id = db.Column(db.String(60), db.ForeignKey('admins.id'))
    transaction_id = db.Column(db.String(20), nullable=False, default=generate_id('TR'))
    bank_transaction_id = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Numeric(precision=20, scale=2), nullable=False)
    type = db.Column(db.Enum(TransactionType), nullable=False)
    status = db.Column(
        db.Enum(TransactionStatus),
        nullable=False,
        default=TransactionStatus.PENDING
    )
