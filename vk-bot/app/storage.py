import asyncio
import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "subscribed_chats.json"
_lock = asyncio.Lock()


def _load() -> dict[str, int]:
    if not DATA_PATH.exists():
        return {}
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def _save(data: dict[str, int]) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


async def set_subscribed(peer_id: int, subscribed: bool) -> None:
    async with _lock:
        data = _load()
        data[str(peer_id)] = 1 if subscribed else 0
        _save(data)


def get_active_peer_ids() -> list[int]:
    data = _load()
    return [int(peer_id) for peer_id, value in data.items() if value == 1]
