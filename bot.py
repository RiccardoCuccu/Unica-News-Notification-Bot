import telegram
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import logging

### Languages ###
import json
import binascii
from lang import lang_it

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)		# you will know when (and why) things don't work as expected

updater = Updater(os.environ['TOKEN'], use_context=True)
dispatcher = updater.dispatcher

### Keyboards ###
standard_keyboard = telegram.ReplyKeyboardMarkup([["Info"], ["Link","Canali","Utility"], ["Donazione"], ["Feedback"], ["Ringraziamenti"]])
base_keyboard = telegram.ReplyKeyboardMarkup([["Utility"]])

### Functions ###
def start(update, context):																					# start with a message
    #context.bot.send_message(chat_id=update.effective_chat.id, text="Benvenuto nel bot di @UnicaNews!\nCome posso esserti utile?")
    context.bot.send_message(chat_id=update.message.chat_id, text="Benvenuto nel bot di @UnicaNews!\nCome posso esserti utile?", reply_markup=standard_keyboard)

def echo(update, context):																					# echo all non-command messages it receives
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def caps(update, context):																					# take some text as an argument and reply to it in CAPS
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def hello(update, context):																					# say "Ciao USER_FIRST_NAME!"
    update.message.reply_text('Ciao {}!'.format(update.message.from_user.first_name))

def unknown(update, context):																				# reply to all commands that were not recognized by the previous handlers
    context.bot.send_message(chat_id=update.effective_chat.id, text="Mi dispiace, questo non e' un comando supportato.")

### Handlers ###
start_handler = CommandHandler('start', start)
dispatcher.add_handler(CommandHandler('start', start))														# responds to the /start command
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))   							# replies to any message without command
dispatcher.add_handler(CommandHandler('caps', caps))														# responds to the /caps command
dispatcher.add_handler(CommandHandler('hello', hello))														# responds to the /hello command
dispatcher.add_handler(MessageHandler(Filters.command, unknown))											# responds to any unknown command

#### INLINE COMMAND ###
#from telegram import InlineQueryResultArticle, InputTextMessageContent
#def inline_caps(update, context):
#    query = update.inline_query.query
#    if not query:
#        return
#    results = list()
#    results.append(
#        InlineQueryResultArticle(
#            id=query.upper(),
#            title='Caps',
#            input_message_content=InputTextMessageContent(query.upper())
#        )
#    )
#    context.bot.answer_inline_query(update.inline_query.id, results)
#
#from telegram.ext import InlineQueryHandler
#inline_caps_handler = InlineQueryHandler(inline_caps)
#dispatcher.add_handler(inline_caps_handler)
########################


updater.start_polling()
updater.idle()
