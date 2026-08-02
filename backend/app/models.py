from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlmodel import Field, SQLModel


class TickKind(str, Enum):
    income = "income"
    expense = "expense"


class Tick(SQLModel, table=True):
    __tablename__ = "payday_ticks"

    id: int | None = Field(default=None, primary_key=True)
    kind: TickKind
    label: str
    amount: Decimal
    balance_after: Decimal
    created_at: datetime


class PaydayState(SQLModel, table=True):
    __tablename__ = "payday_state"

    id: int | None = Field(default=None, primary_key=True)
    balance: Decimal
    updated_at: datetime
