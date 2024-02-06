import asyncio
from django.core.management.base import BaseCommand

from core.apps.bot.main_bot import bot


class Command(BaseCommand):
    help = "Запускаем Телеграм бота"

    def handle(self, *args, **options):
        print('Телеграм бота запущен')
        asyncio.run(bot.polling())
