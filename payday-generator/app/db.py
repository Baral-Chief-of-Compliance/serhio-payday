from decimal import Decimal

import asyncpg

from .config import Settings

_SCHEMA = """
CREATE TABLE IF NOT EXISTS payday_state (
    id SMALLINT PRIMARY KEY DEFAULT 1 CHECK (id = 1),
    balance NUMERIC(16, 2) NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS payday_ticks (
    id BIGSERIAL PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('income', 'expense')),
    label TEXT NOT NULL,
    amount NUMERIC(16, 2) NOT NULL,
    balance_after NUMERIC(16, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""


async def create_pool(settings: Settings) -> asyncpg.Pool:
    return await asyncpg.create_pool(dsn=settings.postgres_dsn, min_size=1, max_size=5)


async def ensure_schema(pool: asyncpg.Pool) -> None:
    async with pool.acquire() as conn:
        await conn.execute(_SCHEMA)


async def load_balance(pool: asyncpg.Pool, start_balance: float) -> Decimal:
    async with pool.acquire() as conn:
        async with conn.transaction():
            row = await conn.fetchrow("SELECT balance FROM payday_state WHERE id = 1 FOR UPDATE")
            if row is not None:
                return row["balance"]
            balance = Decimal(str(start_balance))
            await conn.execute(
                "INSERT INTO payday_state (id, balance) VALUES (1, $1)", balance
            )
            return balance


async def record_tick(
    pool: asyncpg.Pool,
    *,
    kind: str,
    label: str,
    amount: Decimal,
    balance_after: Decimal,
) -> None:
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                "UPDATE payday_state SET balance = $1, updated_at = now() WHERE id = 1",
                balance_after,
            )
            await conn.execute(
                """
                INSERT INTO payday_ticks (kind, label, amount, balance_after)
                VALUES ($1, $2, $3, $4)
                """,
                kind,
                label,
                amount,
                balance_after,
            )
