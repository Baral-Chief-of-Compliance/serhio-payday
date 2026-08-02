from vkbottle.bot import Message

from . import storage
from .bot_instance import bot


@bot.on.message(text=["/start", "start"])
async def start_handler(message: Message) -> None:
    await storage.set_subscribed(message.peer_id, True)
    await message.answer(
        "Рассылка баланса включена для этой беседы — обновления будут приходить раз в час. "
        "Чтобы отключить — /stop"
    )


@bot.on.message(text=["/stop", "stop"])
async def stop_handler(message: Message) -> None:
    await storage.set_subscribed(message.peer_id, False)
    await message.answer("Рассылка отключена. Включить снова — /start")
