from vkbottle.bot import Bot

from .config import Settings

settings = Settings()
bot = Bot(settings.vk_token)
