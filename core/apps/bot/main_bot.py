import logging
import telebot

from telebot.async_telebot import AsyncTeleBot

# from core.core import settings
from django.conf import settings

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='html')


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    print('Привет Друг!!!')
    await bot.reply_to(message, "Привет Друг!!! :)")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    await bot.reply_to(message, message.text)
