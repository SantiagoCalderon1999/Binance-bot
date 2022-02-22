from distutils.command.config import config
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

import telegram_config

#Insert your own 
updater = Updater(telegram_config.API_TOKEN,
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text("First text")