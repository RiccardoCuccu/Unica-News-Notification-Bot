import telegram
from telegram import ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, Filters
import os
import re
import logging

### Languages ###
import json
import binascii
from lang import lang_it

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)		# you will know when (and why) things don't work as expected

token = os.environ['TOKEN']
admin_id = os.environ['ADMIN_ID']

updater = Updater(token, use_context=True)
dispatcher = updater.dispatcher

CHOOSING = 0

### Messages ###
channels_message = 'Canali in ordine alfabetico\n@UnicaNews\n@UnicaNewsAmministrazOrganizzaz\n@UnicaNewsArchitettura\n@UnicaNewsAssistenzaSanitaria\n@UnicaNewsBeniCulturaliSpettacolo\n@UnicaNewsBiologia\n@UnicaNewsBiotecnologieInd\n@UnicaNewsChimica\n@UnicaNewsCTF\n@UnicaNewsEconomiaFinanza\n@UnicaNewsEconomiaGestAziendale\n@UnicaNewsEconomiaGestioneTur\n@UnicaNewsEducazioneProfessionale\n@UnicaNewsFarmacia\n@UnicaNewsFilosofia\n@UnicaNewsFisica\n@UnicaNewsFisioterapia\n@UnicaNewsGiurisprudenza\n@UnicaNewsIgieneDentale\n@UnicaNewsInfermieristica\n@UnicaNewsInformatica\n@UnicaNewsIngegneriaArchitettura\n@UnicaNewsIngAmbienteTerritorio\n@UnicaNewsIngBiomedica\n@UnicaNewsIngChimica\n@UnicaNewsIngCivile\n@UnicaNewsIngEleEleInf\n@UnicaNewsIngElettrica\n@UnicaNewsIngElettronica\n@UnicaNewsIngEnergetica\n@UnicaNewsIngMeccanica\n@UnicaNewsLettere\n@UnicaNewsLingueComunicazione\n@UnicaNewsLingueMediazione\n@UnicaNewsLogopedia\n@UnicaNewsMatematica\n@UnicaNewsMedicinaChirurgia\n@UnicaNewsOstetricia\n@UnicaNewsScienzeAmbientNaturali\n@UnicaNewsScienzeArchitettura\n@UnicaNewsScienzeComunicazione\n@UnicaNewsScienzeEducazione\n@UnicaNewsScienzeFormPrimaria\n@UnicaNewsScienzeGeologiche\n@UnicaNewsScienzeMotorieSportive\n@UnicaNewsScienzeNaturali\n@UnicaNewsScienzePolitiche\n@UnicaNewsScienzePsicologiche\n@UnicaNewsScienzeServiziGiuridici\n@UnicaNewsSEGP\n@UnicaNewsStudiUmanistici\n@UnicaNewsTecnicaRiabPsichiatrica\n@UnicaNewsTecnicheLabBiomedico\n@UnicaNewsTecnichePrevAmbiente\n@UnicaNewsTecnicheRadioMedica\n@UnicaNewsTossicologia'
donations_message = "Unica News non è finanziato dall'Università di Cagliari ma tacitamente accettato da essa, i nostri sviluppatori lavorano senza alcun compenso a questo progetto, per questo se volessi dirgli grazie o semplicemente offrirgli un caffè tramite questo" + ' <a href="https://paypal.me/pools/c/7ZffopI0Eo">link</a> ' + "te ne sarebbero estremamente grati! :)\n\nTi invitiamo a segnalarci tramite il tasto 'Feedback' la tua donazione, se lo vorrai il tuo nome potrà essere aggiunto ai ringraziamenti ufficiali visibili cliccando sul tasto 'Ringraziamenti'."
feedback_entry_message = 'Ora invia il tuo feedback!'
feedback_error_message = 'Errore, sono supportati solo messaggi di testo.'
feedback_sent_message = 'Il tuo feedback:\n\n"{}"\n\nè stato inviato correttamente!'
feedback_undo_message = 'Feedback annullato.'
hello_message = 'Ciao {}!'
help_message = 'Comandi supportati:\n- \\start\n- \\hello\n- \\echo'
info_message = 'Apposito bot per la comunicazione di problemi, consigli o idee del canale @UnicaNews. Scrivici tramite il pulsante "Feedback" (ricorda che non sarà data alcuna risposta riguardo gli orari di lezioni ed esami, essi potranno essere visionati sugli appositi siti di indirizzo).'
link_message = 'Scegli la tua facoltà (al momento solo alcune sono disponibili).'
thanks_message = 'Un ringraziamento speciale per la creazione e il sostegno per questo progetto vanno a:\n- Federica Trenta\n- Carlo Pisano'
unknown_message = "Mi dispiace, questo non è un comando supportato."
utility_message = 'FB Ufficio Dsu ➡️ http://bit.ly/2PPjpFl\nPlugin ESSE3 ➡️ http://bit.ly/34B4UJv\nAmazon Student ➡️ https://amzn.to/34xtfjp\n\nERSU ➡️ @ufficioculturale_Ersu\nCagliariBus News ➡️ @cagliaribusnews\nRegione Sardegna ➡️ @RegioneSardegna\nAVIS UniCa News ➡️ @AVISUniCaNews\nUnicApp Bot ➡️ @UnicAppBot'
welcome_message = 'Benvenuto nel bot di @UnicaNews!\nCome posso esserti utile?'

### Keyboards ###
standard_keyboard = telegram.ReplyKeyboardMarkup([["Info"], ["Link","Canali","Utility"], ["Donazione"], ["Feedback"], ["Ringraziamenti"]])
faculty_keyboard = telegram.ReplyKeyboardMarkup([["Biologia e Farmacia"], ["Economia"], ["Giurisprudenza"], ["Infermieristica"], ["Ingegneria"], ["Medicina e Chirurgia"], ["Scienze"], ["Scienze Politiche"], ["Studi Umanistici"], ["Torna indietro"]])
undo_keyboard = telegram.ReplyKeyboardMarkup([['Annulla']])

### Functions - Commands ###
def start(update, context):																							# start with a message
	context.bot.send_message(chat_id=update.message.chat_id, text=welcome_message, reply_markup=standard_keyboard)

def help(update, context):																							# help with a message
	context.bot.send_message(chat_id=update.message.chat_id, text=help_message, reply_markup=standard_keyboard)

def echo(update, context):																							# echo all non-command messages it receives
	context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text, reply_markup=standard_keyboard)

def caps(update, context):																							# take some text as an argument and reply to it in CAPS
	text_caps = ' '.join(context.args).upper()
	context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps, reply_markup=standard_keyboard)

def hello(update, context):																							# say "Ciao USER_FIRST_NAME!"
	update.message.reply_text(hello_message.format(update.message.from_user.first_name))

def unknown(update, context):																						# reply to all commands that were not recognized by the previous handlers
	context.bot.send_message(chat_id=update.effective_chat.id, text=unknown_message, reply_markup=standard_keyboard)

### Functions - Buttons ###
def display_info(update, context):																					# display info_message
	context.bot.send_message(chat_id=update.message.chat_id, text=info_message, reply_markup=standard_keyboard)

def display_link(update, context):																					# display link_message
	context.bot.send_message(chat_id=update.message.chat_id, text=link_message, reply_markup=faculty_keyboard)

def display_channels(update, context):																				# display channels_message
	context.bot.send_message(chat_id=update.message.chat_id, text=channels_message, reply_markup=standard_keyboard)

def display_utility(update, context):																				# display utility_message
	context.bot.send_message(chat_id=update.message.chat_id, text=utility_message, disable_web_page_preview=True, reply_markup=standard_keyboard)

def display_donations(update, context):																				# display donations_message
	context.bot.send_message(chat_id=update.message.chat_id, text=donations_message, disable_web_page_preview=True, parse_mode=ParseMode.HTML, reply_markup=standard_keyboard)

def display_thanks(update, context):																				# display thanks_message
	context.bot.send_message(chat_id=update.message.chat_id, text=thanks_message, reply_markup=standard_keyboard)

def feedback_entry(update, context):
	update.message.reply_text(feedback_entry_message, reply_markup=undo_keyboard)
	return CHOOSING

def feedback_forwarding(update, context):
	text = update.message.text
	username = update.message.from_user.username
	chat_id = update.message.chat_id
	message = "@"+username+" (ID: "+str(chat_id)+")\n-"+text
	context.bot.send_message(chat_id=admin_id, text=message)
	context.bot.send_message(chat_id=chat_id, text=feedback_sent_message.format(text), reply_markup=standard_keyboard)
	return ConversationHandler.END

def feedback_undo(update, context):
	update.message.reply_text(feedback_undo_message, reply_markup=standard_keyboard)
	return ConversationHandler.END

def feedback_error(update, context):
	update.message.reply_text(feedback_error_message, reply_markup=standard_keyboard)
	return ConversationHandler.END

### Handlers ###
start_handler = CommandHandler('start', start)
dispatcher.add_handler(CommandHandler('start', start))																		# responds to the /start command
dispatcher.add_handler(CommandHandler('help', start))																		# responds to the /start command
dispatcher.add_handler(CommandHandler('caps', caps))																		# responds to the /caps command
dispatcher.add_handler(CommandHandler('hello', hello))																		# responds to the /hello command

dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'^info$', re.IGNORECASE)), display_info))					# responds to the "Info" button
dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'^link$', re.IGNORECASE)), display_link))					# responds to the "Link" button
dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'^canali$', re.IGNORECASE)), display_channels))				# responds to the "Canali" button
dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'^utility$', re.IGNORECASE)), display_utility))				# responds to the "Utility" button
dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'^donazione$', re.IGNORECASE)), display_donations))			# responds to the "Donazione" button
dispatcher.add_handler(MessageHandler(Filters.regex(re.compile(r'^ringraziamenti$', re.IGNORECASE)), display_thanks))		# responds to the "Ringraziamenti" button

dispatcher.add_handler(ConversationHandler(																					# responds to the "Feedback" button
		entry_points=[MessageHandler(Filters.regex(re.compile(r'^feedback$', re.IGNORECASE)), feedback_entry)],
		states={CHOOSING: [	MessageHandler(Filters.regex('^Annulla$'), feedback_undo),
							MessageHandler(Filters.text, feedback_forwarding)]
		},
		fallbacks=[MessageHandler((~Filters.text), feedback_error)]
	)
)

dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))   											# replies to any message without command
dispatcher.add_handler(MessageHandler(Filters.command, unknown))															# responds to any unknown command


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
