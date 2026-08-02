import json
import random
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path


@dataclass(frozen=True)
class Entry:
    label: str
    min: float
    max: float


def load_entries(path: Path) -> list[Entry]:
    items = json.loads(path.read_text(encoding="utf-8"))
    return [Entry(label=item["label"], min=item["min"], max=item["max"]) for item in items]


def pick_amount(entry: Entry) -> Decimal:
    value = random.uniform(entry.min, entry.max)
    return Decimal(str(round(value, 2)))
