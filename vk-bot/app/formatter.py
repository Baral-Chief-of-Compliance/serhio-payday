from decimal import Decimal


def format_amount(value: str | float | Decimal) -> str:
    amount = Decimal(str(value))
    sign = "-" if amount < 0 else ""
    whole, _, frac = f"{abs(amount):.2f}".partition(".")
    whole_with_commas = f"{int(whole):,}"
    return f"{sign}${whole_with_commas}.{frac}"


def format_summary_message(balance: dict, ticks: list[dict]) -> str:
    lines = [
        f"💰 Текущий баланс: {format_amount(balance['balance'])}",
        "",
        f"Последние {len(ticks)} событий:"
    ]
    for i, tick in enumerate(ticks, start=1):
        sign = "+" if tick["kind"] == "income" else "-"
        lines.append(f"{i}. {sign}{format_amount(tick['amount'])} — {tick['label']}")

    return "\n".join(lines).join("\n❗❗ Напоминаем, что наблюдать можно на https://serhio.payday.polartitan.ru/")