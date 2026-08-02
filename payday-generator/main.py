import asyncio
import logging

import httpx

from app import db
from app.config import Settings
from app.data import load_entries
from app.ticker import run_ticker

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


async def main() -> None:
    settings = Settings()

    income_entries = load_entries(settings.income_data_path)
    expense_entries = load_entries(settings.expenses_data_path)

    pool = await db.create_pool(settings)
    await db.ensure_schema(pool)

    try:
        async with httpx.AsyncClient() as http_client:
            await run_ticker(pool, http_client, settings, income_entries, expense_entries)
    finally:
        await pool.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Stopped.")
