import logging

import httpx

from .config import Settings

logger = logging.getLogger(__name__)


async def publish_tick(client: httpx.AsyncClient, settings: Settings, payload: dict) -> None:
    if not settings.centrifugo_enabled:
        return
    try:
        response = await client.post(
            settings.centrifugo_api_url,
            headers={
                "X-API-Key": settings.centrifugo_api_key,
                "Content-Type": "application/json",
            },
            json={
                "method": "publish",
                "params": {"channel": settings.centrifugo_channel, "data": payload},
            },
            timeout=3.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        logger.warning("Centrifugo publish failed: %s", exc)
