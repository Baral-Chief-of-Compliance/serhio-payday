import logging

from vkbottle import interval

from app import handlers  # noqa: F401  (registers /start, /stop message handlers)
from app.bot_instance import bot, settings
from app.tasks import broadcast_to_chats, post_wall_update

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


@interval(seconds=settings.chat_broadcast_interval_seconds)
async def chat_broadcast_task() -> None:
    await broadcast_to_chats(bot.api, settings)


@interval(seconds=settings.wall_post_interval_seconds)
async def wall_post_task() -> None:
    await post_wall_update(bot.api, settings)


if __name__ == "__main__":
    bot.startup_tasks.append(chat_broadcast_task())
    bot.startup_tasks.append(wall_post_task())
    bot.run()
