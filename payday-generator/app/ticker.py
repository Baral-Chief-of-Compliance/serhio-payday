import asyncio
import logging
import random

import asyncpg
import httpx

from . import centrifugo, db
from .config import Settings
from .data import Entry, pick_amount

logger = logging.getLogger(__name__)


async def run_ticker(
    pool: asyncpg.Pool,
    http_client: httpx.AsyncClient,
    settings: Settings,
    income_entries: list[Entry],
    expense_entries: list[Entry],
) -> None:
    balance = await db.load_balance(pool, settings.start_balance)
    logger.info("Starting balance: $%s", balance)

    while True:
        await asyncio.sleep(random.uniform(settings.tick_min_seconds, settings.tick_max_seconds))

        is_income = random.random() < settings.income_probability
        entry = random.choice(income_entries if is_income else expense_entries)
        amount = pick_amount(entry)
        balance = balance + amount if is_income else balance - amount
        kind = "income" if is_income else "expense"

        await db.record_tick(pool, kind=kind, label=entry.label, amount=amount, balance_after=balance)

        sign = "+" if is_income else "-"
        logger.info("%s$%s  %s  -> balance: $%s", sign, amount, entry.label, balance)

        await centrifugo.publish_tick(
            http_client,
            settings,
            {
                "kind": kind,
                "label": entry.label,
                "amount": str(amount),
                "balance": str(balance),
            },
        )
