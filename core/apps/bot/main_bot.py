import logging
import time
from pprint import pprint

import requests
import telebot
from telebot import async_telebot, types
from telebot.async_telebot import AsyncTeleBot

from django.conf import settings

from apps.bot.tron import get_hash_detail_information

# from core.apps.management.management.commands.run_bot import Command

bot = AsyncTeleBot(settings.TOKEN_BOT, parse_mode='html')
async_telebot.logger.setLevel(settings.LOG_LEVEL)

logger = logging.getLogger(__name__)  # Что бы получать логирование нужно в settings.py установить dic: LOGGING = {....}


def date_time_convert(date):
    return time.strftime("%d.%m.%Y-%H:%M", time.localtime(date))


# def get_hash_information():
#     base_url = "https://apilist.tronscan.org/api"
#     endpoint = f"/transaction-info?"
#     params = {
#         "hash": '81f72eee33bb65751e730e8562807ded95c2fff7fe1bdffeca7c8db7f36ea00c',  # Your transaction hash here.
#         "api_key": settings.TRONSCAN,  # Include your Tronscan API key here
#     }
#     try:
#         response = requests.get(base_url + endpoint, params=params)
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             print(f"Failed to fetch Data. Status code: {response.status_code}")
#             return None
#     except requests.exceptions.RequestException as e:
#         print("Error:", e)
#         return None


@bot.chat_member_handler()
# для того что бы работало нужно в asyncio.run(bot.infinity_polling(ПЕРЕДАТЬ allowed_updates=util.update_types)
async def chat_member_handler_bot(message):  # ChatMemberUpdated' object (message) has no attribute 'json'.
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    username = message.from_user.username
    status = message.difference.get('status')
    # via_chat_folder_invite_link = message.via_chat_folder_invite_link
    date_time = date_time_convert(message.date)

    # print(f'{user_id=}')
    # print(f'{full_name=}')
    # print(f'{username=}')
    # print(f'{status=}')
    # # print(f'{via_chat_folder_invite_link=}')
    # print(f'Дата-Время: {date_time}')

    chat = message.chat.id
    chat_title = message.chat.title
    chat_type = message.chat.type
    # print(f'{chat=}')
    # print(f'{chat_title=}')
    # print(f'{chat_type=}')

    new_chat_member_status = message.new_chat_member.status
    new_chat_member_user_full_name = message.new_chat_member.user.full_name
    new_chat_member_user_id = message.new_chat_member.user.id
    new_chat_member_user_username = message.new_chat_member.user.username
    # print(f'{new_chat_member_status=}')
    # print(f'{new_chat_member_user_full_name=}')
    # print(f'{new_chat_member_user_id=}')
    # print(f'{new_chat_member_user_username=}')

    invite_link = message.invite_link
    link_info_msg = ''
    try:
        invite_link_name = getattr(invite_link, 'name')
        invite_link_url = getattr(invite_link, 'invite_link')
        invite_link_creator_id = getattr(invite_link, 'creator.id')
        invite_link_creator_first_name = getattr(invite_link, 'creator.first_name')
        link_info_msg = f'Invite link URL: {invite_link_url}\n'
        link_info_msg += (f'Invite Link Name: {invite_link_name}\n'
                          f' Создал ссылку: {invite_link_creator_first_name},'
                          f' ID: {invite_link_creator_id}')
        # print(link_info_msg)
    except AttributeError as err:
        logger.info(f'Нет ссылки: {err}')

    text_msg = ('Имя: {}\n' 'User_id: {}\n'.format(new_chat_member_user_full_name,
                                                   new_chat_member_user_id))
    if new_chat_member_user_username:
        text_msg += 'Username: @{}\n'.format(new_chat_member_user_username, )

    msg_header = ''
    if new_chat_member_status == 'member' or new_chat_member_status == 'creator':
        new_chat_member_status = 'Подписан ✅'
        msg_header = '🎉 Ура! Встречай, новый 🐻‍❄️'
    elif new_chat_member_status == 'kicked':
        new_chat_member_status = f'Отправлен в бан 🚽\n Кто удалил: {full_name}'
        msg_header = 'Нашлась 💩 смыли в 🚽'
    elif new_chat_member_status == 'left':
        new_chat_member_status = 'Отписан ❌'
        msg_header = '🙁 До свидания  товарищ!️'

    text_msg += '{}\n'.format(new_chat_member_status)

    if chat_type == 'channel':
        chat_type = 'Канал: '
    elif chat_type == 'supergroup':
        chat_type = 'Чат: '

    text_msg += '{}''{}\n''Дата-Время: {}\n'.format(chat_type, chat_title, date_time)

    logger.info(f'\n ВСЯ ИНФОРМАЦИЯ: \n {message}')
    # await bot.send_message(message.chat.id, "Новый подписчик ")  # Кидает видимое всем сообщение и в канал и в чат.
    await bot.send_message(chat_id=settings.ADMIN_ID,
                           text='{}\n''{}' '{}'.format(msg_header, text_msg,
                                                       link_info_msg))  # Кидает только мне сообщение в Бот.


@bot.message_handler(commands=['start'])
async def start(message):
    markup = types.InlineKeyboardMarkup()
    main_btn = types.InlineKeyboardButton('Вступить в закрытый чат "Крипторелакс"', callback_data='subscribe')
    markup.row(main_btn)

    user_id = message.from_user.id
    username = message.from_user.username
    user_full_name = message.from_user.full_name
    text = message.text

    date_time = date_time_convert(message.date)

    # greting = f'<b>{from_user_full_name}</b>'
    mes_1 = (f'<b> Я 🤖 умею отправлять ссылку для вступления в закрытый чат "Крипторелакс"\n'
             f' но сначала подпишись на youtube канал</b>')
    cryptorelax = "{:-^31}".format('КРИПТОРЕЛАКС')
    link_youtube = f'<b><a href="https://www.youtube.com/@Crypto-Relax">{cryptorelax}</a></b>'
    message_text = f'<b>{user_full_name}, привет! \n {mes_1} \n {link_youtube}</b>'

    await bot.send_message(message.chat.id, message_text, reply_markup=markup)

    print(f'{user_id=}')
    print(f'{username=}')
    print(f'{user_full_name=}')
    print(f'Дата-Время: {date_time}')

    logger.info(f'\n ВСЯ ИНФОРМАЦИЯ: \n {message}')
    # pprint(message.json)

    await bot.send_message(settings.ADMIN_ID, f"From user: {user_full_name}\n "
                                              f"текст: {message.text}")  # Отправляет сообщение в бот Админу.
    print("stop")


@bot.callback_query_handler(func=lambda callback: True)
async def callback_message(callback):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('90 дней - 125$', callback_data='days_90_payment_125')
    btn3 = types.InlineKeyboardButton('180 дней - 200$', callback_data='days_180_payment_200')
    btn4 = types.InlineKeyboardButton('360 дней - 350$', callback_data='days_360_payment_350')
    btn5 = types.InlineKeyboardButton('720 дней - 600$', callback_data='days_720_payment_600')
    markup.row(btn2, btn3)
    markup.row(btn4, btn5)

    full_name = callback.from_user.full_name
    announcement = f'{full_name},\n Выберите тариф для вступления в закрытый чат "Крипторелакс".'
    discount = f'Скидка: \n <span class="tg-spoiler">  - 20% на 180 дней, \n   - 30% на 360 дней, \n   - 40% на 720 дней</span>'
    msg = f'<b> {announcement}</b> \n\n {discount}'

    if callback.data == 'subscribe':
        await bot.send_message(callback.message.chat.id, msg, reply_markup=markup)

    # text_1 = f'Сделайте перевод 💸 <b>USDT</b> в сети <b>Tron (TRC20)</b> на адрес: \n'
    # address_wallet = '{:-^31}'.format('<code>THzdCHJv1SWpkWk9jND3iEoKKYHNkJN5Kj</code>\n 👆 нажать - скопировать 👆')
    # text_2 = f'<i>\n Для проверки платежа после оплаты, отправьте хэш транзакции в чат. 👇</i>'

    payment = None
    if callback.data == 'days_90_payment_125':
        payment = 125
    elif callback.data == 'days_180_payment_200':
        payment = 200
    elif callback.data == 'days_360_payment_350':
        payment = 350
    elif callback.data == 'days_720_payment_600':
        payment = 600

    text_1 = f'Сделайте перевод 💸 <b>{payment} USDT</b> в сети <b>Tron (TRC20)</b> на адрес: \n'
    address_wallet = '{:-^31}'.format('<code>THzdCHJv1SWpkWk9jND3iEoKKYHNkJN5Kj</code>\n 👆 нажать - скопировать 👆')
    text_2 = f'<i>\n Для проверки платежа после оплаты, отправьте хэш транзакции в чат. 👇</i>'

    if payment:
        await bot.send_message(callback.message.chat.id, f'{text_1} {address_wallet} {text_2}')

    # logger.info(f'\n ВСЯ ИНФОРМАЦИЯ: \n {callback}')

    user_id = callback.from_user.id
    print(f'user_id: {user_id}')
    date = date_time_convert(callback.message.date)
    print(f'Дата, Время: {date}')
    data = callback.data
    print(f'Для БД: data: {data}')


@bot.message_handler(regexp=r'^[0-9a-fA-F]{64}$')
async def handle_trc20_hash_message(message):
    """ Регулярное выражение обрабатывает строку по шаблону хеша транзакции в Tron TRC20.
        Должна начинаться и заканчиваться (^ и $) и содержать 64 символа в шестнадцатеричном формате ([0-9a-fA-F]).
    """
    user_id = message.from_user.id
    print(f'user_id: {user_id}')
    user_name = message.from_user.username

    hash_tron = message.html_text
    print(f'Hash Tron: {hash_tron}')

    date = date_time_convert(message.date)
    print(f'Дата, Время: {date}')

    await bot.send_message(message.chat.id, f'{hash_tron} - Hash принят.')
    await bot.send_dice(message.chat.id)

    # Отправляет сообщение в бот Админу.
    await bot.send_message(settings.ADMIN_ID, f'🤖 >>> Админу: {date} \n Новый запрос от\n User ID: {user_id}'
                                              f'\nUser name: {user_name} \n{hash_tron} - Hash транзакции Tron.')

    # Код, который обрабатывает сообщение с хешем транзакции в Tron TRC20
    hash_data = get_hash_detail_information(hash_tron, settings.TRON_SCAN)
    # pprint(data)
    if hash_data:
        confirmations = hash_data['confirmations']
        timestamp = hash_data['timestamp']
        from_address = hash_data['tokenTransferInfo']['from_address']
        to_address = hash_data['tokenTransferInfo']['to_address']
        symbol = hash_data['tokenTransferInfo']['symbol']
        tokenType = hash_data['tokenTransferInfo']['tokenType']
        type = hash_data['tokenTransferInfo']['type']
        amount = int(hash_data['tokenTransferInfo']['amount_str'])
        decimals = hash_data['tokenTransferInfo']['decimals']
        amount = int(amount) / int(("1" + "0" * decimals))

        print(f'Status confirmations: {confirmations}')
        date_time_local_timestamp = time.localtime(timestamp / 1000)
        date_time_transaction_local = time.strftime("%d.%m.%Y-%H.%M.%S", date_time_local_timestamp)
        print(f'{type}, From address: {from_address}')
        print(f'Value: {amount} {symbol} ({tokenType})')
        print(f'{type}, To address: {to_address}')
        answer_from_tron_scan = f'\n Date & Time of transaction (local): {date_time_transaction_local}' \
                                f'\n Status confirmations: {confirmations} ' \
                                f'\n {type} с адреса: {from_address} ' \
                                f'\n Value: {amount} {symbol} ({tokenType}) ' \
                                f'\n {type}, To address: {to_address}'
        print(answer_from_tron_scan)




# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
async def echo_message(message):
    # pprint(message.json)  # Аргумент json есть в message, работает.
    # logger.info(f'\n ВСЯ ИНФОРМАЦИЯ: \n {message}')
    await bot.reply_to(message, message.text)
    await bot.send_message(settings.ADMIN_ID, f"Текст от user: {message.from_user.full_name}\n "
                                              f"текст: {message.text}")  # Кидает только мне сообщение в Бот.
