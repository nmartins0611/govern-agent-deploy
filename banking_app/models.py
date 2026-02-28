"""Database models for the banking application"""

from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Enum
from sqlalchemy.orm import declarative_base, sessionmaker
import enum
import uuid

Base = declarative_base()


class TransactionType(enum.Enum):
    """Transaction type enumeration"""
    TRANSFER = "transfer"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"


class TransactionStatus(enum.Enum):
    """Transaction status enumeration"""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class Account(Base):
    """Account model"""
    __tablename__ = 'accounts'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    account_number = Column(String(20), unique=True, nullable=False)
    holder_name = Column(String(100), nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    currency = Column(String(3), default='USD', nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Account {self.account_number} - {self.holder_name}>"


class Transaction(Base):
    """Transaction model"""
    __tablename__ = 'transactions'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    from_account_id = Column(String, nullable=True)
    to_account_id = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    status = Column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<Transaction {self.id} - {self.transaction_type.value}>"
