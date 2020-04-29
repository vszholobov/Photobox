from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
import bot_functions


list_of_commands = []
commands = []
last_message = None

for key in bot_functions.activators:
    list_of_commands.append(bot_functions.Commands(bot_functions.activators[key],
                                                   list(map(bot_functions.add_person,
                                                            bot_functions.answers[key]))))
    commands.extend(bot_functions.activators[key])

print("Бот запущен")


def message_handler(bot: Bot, update: Update):

    global last_message
    message = bot_functions.analyze_text(update.effective_message.text.lower().replace(' ', ''), commands)

    if update.effective_message.text == last_message:
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text=bot_functions.last_random_message())
    elif message == "Nope":
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text=bot_functions.random_nope_message())
    else:
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text=bot_functions.find_command(message, list_of_commands))

    last_message = update.effective_message.text


bot = Bot(token="1254233101:AAHhRM7bqItByr5Au621sNXoxyH4WIAc4NM")
updater = Updater(bot=bot)
handler = MessageHandler(Filters.all, message_handler)
updater.dispatcher.add_handler(handler)

updater.start_polling()
updater.idle()
