import asyncio
import logging


from django.core.management.base import BaseCommand
from telebot import util

from core.apps.bot.main_bot import bot

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Запускаем Телеграм бота"

    def handle(self, allowed_updates=None, *args, **options):
        print('Телеграм бота запущен')
        try:
            asyncio.run(bot.infinity_polling(allowed_updates=util.update_types))
            # asyncio.run(bot.infinity_polling())
        except Exception as err:
            print(err)
            logger.error(f'Ошибка: {err}')