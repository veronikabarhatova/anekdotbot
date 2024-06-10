import requests
import json
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater
import logging
import os
from dotenv import load_dotenv

load_dotenv()

secret_token = os.getenv('TOKEN')
chat_id = os.getenv('CHAT_ID')
URL = 'http://rzhunemogu.ru/RandJSON.aspx?CType=1'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_new_anekdot():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'http://rzhunemogu.ru/RandJSON.aspx?CType=2'
        response = requests.get(new_url)
    cleaned_response = ''.join(filter(lambda x: x.isprintable(),
                                      response.text))
    data = json.loads(cleaned_response)
    content_value = data.get('content')
    return content_value


def new_anekdot(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, text=get_new_anekdot())


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/new_anekdot']], resize_keyboard=True)
    context.bot.send_message(chat_id=chat.id,
                             text='Привет, {}. Посмотри, какой анекдот я нашёл'
                             .format(name),
                             reply_markup=button)
    context.bot.send_message(chat.id, text=get_new_anekdot())


def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('new_anekdot', new_anekdot))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
