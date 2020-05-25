from telegram import Bot
from telegram import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
import requests
import copy
import bot_functions


list_of_commands = []
commands = []
last_message = None
level_of_keyboard = 0
choose_keyboard = []
list_of_photos = []


for key in bot_functions.activators:
    list_of_commands.append(bot_functions.Commands(bot_functions.activators[key],
                                                   list(map(bot_functions.add_person,
                                                            bot_functions.answers[key]))))
    commands.extend(bot_functions.activators[key])

print("Бот запущен")


def create_keyboard(min_border, max_border):
    """
    Функция создает клавиатуру, которая выведется пользователю.

    :param min_border: минимальное значение диапазона клавиатуры.
    :param max_border: максимальное значение диапазона клавиатуры.
    :return: квавиатура в виде списка списков.
    """
    keyboard = []
    degree = len(str(max_border)) - 2
    if max_border - min_border <= 100:
        degree = 1
    curr_max_border = min_border
    while curr_max_border + pow(10, degree) <= max_border:
        if curr_max_border == min_border:
            keyboard.append([f'{min_border} - {min_border + pow(10, degree) - min_border % pow(10, degree)}'])
            curr_max_border = min_border + pow(10, degree) - min_border % pow(10, degree) + 1
        else:
            keyboard.append([f'{curr_max_border} - {curr_max_border + pow(10, degree) - 1}'])
            curr_max_border += pow(10, degree)
    if curr_max_border < max_border:
        keyboard.append([f'{curr_max_border} - {max_border}'])

    if int(keyboard[-1][0].split(" ")[2]) == max_border - 1:
        keyboard.append([f'{max_border}'])

    return keyboard


def random_search(bot: Bot, update: Update):
    """
    Функция делает запрос на сервер и отправляет случайную фотографию пользователю.

    :param bot: объект бота.
    :param update: объект update.
    """
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "random"})
    json_response = response.json()
    print(json_response["route"])
    bot.send_photo(chat_id=update.effective_message.chat_id,
                   photo=open(json_response["route"], 'rb'))


def tag_search(message, chat_id):
    """
    Функция делает запрос на сервер и возвращает список директорий подходящих к тэгам фотографий.

    :param message: сообщение пользователя.
    :param chat_id: индентификатор пользователя.
    :return: список директорий к фотографиям, если есть хотя бы одна фотография
    """
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "tags", "tags": message})
    json_response = response.json()
    if len(json_response["routes"]) < 1:
        return 0
    else:
        if bot_functions.create_photo_matrix(json_response["routes"], chat_id) is True:
            return json_response["routes"]
        else:
            return 0


def send_photo(bot: Bot, update: Update, first_keyboard):
    """
    Функция заставляет бота отправить фотографию пользователю.

    :param bot: объект бота.
    :param update: объект update.
    :param first_keyboard: стартовая клавиатура.
    """
    global list_of_photos
    bot.send_message(chat_id=update.effective_message.chat_id, text="Совпадений не найдено ;(",
                     reply_markup=ReplyKeyboardMarkup(first_keyboard, one_time_keyboard=True,
                                                      resize_keyboard=True))

    bot.send_photo(chat_id=update.effective_message.chat_id,
                   photo=open(list_of_photos[int(update.effective_message.text) - 1], "rb"),
                   reply_markup=ReplyKeyboardMarkup(first_keyboard, one_time_keyboard=True,
                                                    resize_keyboard=True))


def message_handler(bot: Bot, update: Update):
    """
    Функция обработки сообщений, приходящих от пользователя.

    :param bot: объект бота.
    :param update: объект update.
    """

    first_keyboard = [["Сайт", "Random"]]
    global last_message
    global level_of_keyboard
    global choose_keyboard
    global list_of_photos

    if level_of_keyboard > 0:
        if level_of_keyboard == 1:
            for i in range(len(choose_keyboard)):
                if update.effective_message.text in choose_keyboard[i]:
                    send_photo(bot, update, first_keyboard)
            level_of_keyboard -= 1

        else:
            for i in range(len(choose_keyboard)):
                if update.effective_message.text in choose_keyboard[i]:
                    borders = update.effective_message.text.split(" ")
                    if int(borders[2]) - int(borders[0]) < 10:
                        choose_keyboard = []
                        for k in range(int(borders[0]), int(borders[2]) + 1):
                            choose_keyboard.append([f'{k}'])
                    else:
                        choose_keyboard = copy.deepcopy(create_keyboard(int(borders[0]), int(borders[2])))
                    bot.send_message(chat_id=update.effective_message.chat_id, text="Похоже нужно продолжать",
                                     reply_markup=ReplyKeyboardMarkup(choose_keyboard,
                                                                      one_time_keyboard=True, resize_keyboard=True))
                    level_of_keyboard -= 1

    else:
        if "#" in update.effective_message.text:
            list_of_photos = copy.deepcopy(tag_search(update.effective_message.text, update.effective_message.chat_id))
            if len(list_of_photos) != 0:
                count_of_images = len(tag_search(update.effective_message.text, update.effective_message.chat_id))
            else:
                count_of_images = 0
            last_message = update.effective_message.text
            buffer_count = count_of_images
            if count_of_images == 0:
                bot.send_message(chat_id=update.effective_message.chat_id, text="Совпадений не найдено ;(",
                                 reply_markup=ReplyKeyboardMarkup(first_keyboard, one_time_keyboard=True,
                                                                  resize_keyboard=True))
            else:
                level_of_keyboard = 1
                while buffer_count // 10 > 0:
                    buffer_count = buffer_count // 10
                    level_of_keyboard += 1
                bot.send_photo(chat_id=update.effective_message.chat_id,
                               photo=open(f'{update.effective_message.chat_id}.jpg', "rb"))
                if count_of_images > 10:
                    choose_keyboard = create_keyboard(1, count_of_images)
                    bot.send_message(chat_id=update.effective_message.chat_id, text="Похоже нужно продолжать",
                                     reply_markup=ReplyKeyboardMarkup(choose_keyboard,
                                                                      one_time_keyboard=True, resize_keyboard=True))
                else:
                    choose_keyboard = []
                    for i in range(1, count_of_images + 1):
                        choose_keyboard.append([f'{i}'])
                    bot.send_message(chat_id=update.effective_message.chat_id, text="Похоже нужно продолжать",
                                     reply_markup=ReplyKeyboardMarkup(choose_keyboard,
                                                                      one_time_keyboard=True, resize_keyboard=True))
        else:
            message = bot_functions.analyze_text(update.effective_message.text.lower().replace(' ', ''), commands)

            if update.effective_message.text == "/start":
                bot.send_message(chat_id=update.effective_message.chat_id, text="приветствую",
                                 reply_markup=ReplyKeyboardMarkup(first_keyboard, one_time_keyboard=True,
                                                                  resize_keyboard=True))
            elif update.effective_message.text == "Random":
                bot.send_message(chat_id=update.effective_message.chat_id, text="Дайте секундочку...",
                                 reply_markup=ReplyKeyboardMarkup(first_keyboard, one_time_keyboard=True,
                                                                  resize_keyboard=True))
                random_search(bot, update)
            elif update.effective_message.text == "Сайт":
                bot.send_message(chat_id=update.effective_message.chat_id, text="https://photobox.pythonanywhere.com",
                                 reply_markup=ReplyKeyboardMarkup(first_keyboard, one_time_keyboard=True,
                                                                  resize_keyboard=True))
            elif update.effective_message.text == last_message:
                bot.send_message(chat_id=update.effective_message.chat_id,
                                 text=bot_functions.last_random_message())
            elif message == "Nope":
                bot.send_message(chat_id=update.effective_message.chat_id,
                                 text=bot_functions.random_nope_message())
            else:
                bot.send_message(chat_id=update.effective_message.chat_id,
                                 text=bot_functions.find_command(message, list_of_commands))


if __name__ == '__main__':

    bot = Bot(token="1254233101:AAHhRM7bqItByr5Au621sNXoxyH4WIAc4NM")
    updater = Updater(bot=bot)
    handler = MessageHandler(Filters.all, message_handler)
    updater.dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()
