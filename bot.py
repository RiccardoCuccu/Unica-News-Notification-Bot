from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import os
import re
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

#def start(update, context):
#    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    
#Send a message when the command /start is issued
def start(bot, update):
    update.message.reply_text('Hi!')

def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def bup(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)

def main():
    updater = Updater(os.environ['TOKEN'])
    dispatcher = updater.dispatcher
    
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    
    dispatcher.add_handler(CommandHandler('bop',bop))
    dispatcher.add_handler(CommandHandler('bup',bup))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
