#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import configparser

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename='connectTeamBot.log')

logger = logging.getLogger(__name__)

def getDutyName():
    file = open("duty_name.txt", 'r')
    return file.readline().decode("UTF-8")

def setDutyName(newName):
    file = open("duty_name.txt", 'w')
    file.write(newName.encode("UTF-8"))

def set_duty(bot, update, args):
    printCommandLog('Set_duty', update.message.from_user)

    if len(args) == 1:
        setDutyName(args[0])
        bot.sendMessage(update.message.chat_id, text = "Новое имя установлено")
        logger.info('New name %s', args[0])
    else:
        bot.sendMessage(update.message.chat_id, text = "Неправильный параметр команды")

def get_duty(bot, update, args):
    printCommandLog('Get_duty', update.message.from_user)

    dutyName = getDutyName()
    bot.sendMessage(update.message.chat_id, text=dutyName)

def start(bot, update):
    printCommandLog('Start', update.message.from_user)

    bot.sendMessage(update.message.chat_id, text='Привет')

def help(bot, update):
    printCommandLog('Help', update.message.from_user)
    bot.sendMessage(update.message.chat_id, text='Написать "дежурный" или /get_duty чтобы получить имя.')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def freeText(bot, update):
    printCommandLog('Free text', update.message.from_user)
    inputText = update.message.text
    if inputText == "дежурный".decode('utf-8'):
        dutyName = getDutyName()
        bot.sendMessage(update.message.chat_id, text=dutyName)

def printCommandLog(commandName, user):
    logger.info(commandName + ' command. User %s %s (username %s, id %d)', user.first_name, user.last_name, user.username, user.id)


def main():
    config = configparser.ConfigParser()
    config.read("connectTeamBot.config", encoding='utf8')
    token = config['main']['telegram_token']
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("set_duty", set_duty, pass_args=True))
    dp.add_handler(CommandHandler("get_duty", get_duty, pass_args=True))

    free_text_handler = MessageHandler(Filters.text, freeText)
    dp.add_handler(free_text_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
