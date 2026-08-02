import asyncio
import logging
import random

from vkbottle.api import API

from . import storage
from .config import Settings
from .formatter import format_summary_message
from .ticker_client import fetch_balance, fetch_ticks

logger = logging.getLogger(__name__)

_group_owner_id: int | None = None


async def _build_message(settings: Settings) -> str:
    balance, ticks = await asyncio.gather(
        fetch_balance(settings.api_base),
        fetch_ticks(settings.api_base),
    )
    return format_summary_message(balance, ticks)


async def broadcast_to_chats(api: API, settings: Settings) -> None:
    try:
        text = await _build_message(settings)
    except Exception:
        logger.exception("Failed to build chat broadcast message")
        return

    peer_ids = storage.get_active_peer_ids()
    logger.info("Broadcasting update to %d subscribed chats", len(peer_ids))

    for peer_id in peer_ids:
        try:
            await api.messages.send(
                peer_id=peer_id,
                message=text,
                random_id=random.randint(-2_147_483_648, 2_147_483_647),
            )
        except Exception:
            logger.exception("Failed to send message to peer_id=%s", peer_id)
        await asyncio.sleep(0.35)


async def post_wall_update(api: API, settings: Settings) -> None:
    global _group_owner_id

    try:
        text = await _build_message(settings)
    except Exception:
        logger.exception("Failed to build wall post message")
        return

    if _group_owner_id is None:
        groups_response = await api.groups.get_by_id()
        if not groups_response.groups:
            logger.error("Could not resolve community id for wall post")
            return
        _group_owner_id = -groups_response.groups[0].id

    try:
        await api.wall.post(owner_id=_group_owner_id, message=text, from_group=True)
        logger.info("Posted wall update")
    except Exception:
        logger.exception("Failed to post wall update")
