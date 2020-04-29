from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
import random
from bot_functions import analyze_text, add_person, create_photo_matrix, Commands, find_command


def random_last_message():
    message = ["Ты повторился", "Опять", "Вроде не смешно", "Повторение", "Я почему-то вижу эхо", "Отзвук"]
    return random.choice(message)


def random_reiteration_message():
    message = ["Не смог распознать", "Анализ произошел неудачно", "Знаю тысячи языков, но это не смог распознать",
               "Сложные буквы", "Ты повторился", "Опять", "Вроде не смешно", "Повторение", "Я почему-то вижу эхо",
               "Отзвук"]
    return random.choice(message)


token = "845b43c4cd5c2b81f14efc3d0e878581dd6245acba70292db1c9a55d0d76fe252207e10f1842b8bcf40da"

activators = {
    "привет": ["привет", "здравствуй"],
    "пока": ["прощай", "пока", "досвидания"],
    "какдела?": ["какдела?"],
    "ктоты?": ["ктоты?"],
    "случайно": ["случайно", "рандом"],
    "фотобокс": ["фотобокс"],
    "создатель": ["ктотебясоздал"],
    "сайт": ["сайт", "ссылка"],
    "фото": ["фото", "фотография", "картинка"],
    "команды": ["команда", "чтотыумеешь", "управление"],
    "икит": ["икит"],

}

answers = {
    "привет": ["Привет", "Х-а-а-а-й", "Здравствуй", "Гутен таг", "Дратути"],
    "пока": ['Пока', 'Аривидерчи', 'Гуд бай', 'До свидания', 'Покеда'],
    "какдела?": ["Положительно. Но мое мнение может поменяться", "Отлично думаю",
                 "Работаю на Фотобокс", "Нормально, роботизирую процессы", "Всё ок",
                 "Окей", "Амбивалентно", "Как у колобка — слева и справа одинаково"],
    "ктоты?": ["Робот", "Машина", "Бот, Джеймс Бот", "Точно не человек", "Твой помощник",
               "Работник Фотобокс, сисадмин", "Существо, обитающее в ВКонтакте"],
    "случайно": ["случайно"],
    "фотобокс": ["Место, где я работаю", "Мой дом", "Здесь меня собрали", "Люблю фотобокс", "Выдает картиночки",
                 "Хранитель фотографий"],
    "создатель": [""],
    "сайт": ["Держи: http://photobox.pythonanywhere.com/ - это сайт"],
    "фото": ["У меня нет глаз, но их двоичный код прекрасен", "Это ты можешь загрузить на фотобокс",
             "Только если в цифровом формате"],
    "команды": ["Ты можешь ввести спомощью '#' слова и я постараюсь найти фото по этим хештэгам"],
    "икит": ["Прерасное место", "Жить без него не могу", "Там программируют"],
}

emoji = [" &#128526;", " &#129313;", " &#128522;", " &#128515;", " &#128521;", " &#128518;", " &#129302;",
         " &#128373;", " &#128529;", " &#128567;", " &#128519;", " &#128169;", " &#128527;", " &#128517;",
         " &#128524;", " &#128516;", " &#129315;", " &#129300;", " &#128578;", " &#128513;", " &#128512;",
         " &#9786;", " &#128540;", " &#128514;"]

list_of_commands = []
commands = []
last_message = None

for key in activators:
    list_of_commands.append(Commands(activators[key], list(map(add_person, answers[key]))))
    commands.extend(activators[key])

print("Бот запущен")


def message_handler(bot: Bot, update: Update):

    global last_message
    message = analyze_text(update.effective_message.text.lower().replace(' ', ''), commands)

    if update.effective_message.text == last_message:
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text="Где-то я это уже слышал...")
    elif message == "Nope":
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text="Похоже это не для моего понимая")
    else:
        bot.send_message(chat_id=update.effective_message.chat_id,
                         text=find_command(message, list_of_commands))

    last_message = update.effective_message.text


bot = Bot(token="1254233101:AAHhRM7bqItByr5Au621sNXoxyH4WIAc4NM")
updater = Updater(bot=bot)
handler = MessageHandler(Filters.all, message_handler)
updater.dispatcher.add_handler(handler)

updater.start_polling()
updater.idle()
