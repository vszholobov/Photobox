import vk_api
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from bot_functions import analyze_text, add_person, create_photo_matrix, Commands, find_command


def tag_search(user, message, emoji):
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "tags", "tags": message})
    json_response = response.json()
    if len(json_response["routes"]) < 1:
        write_msg(user, "Ничего не нашёл, человек", emoji)
        return []
    else:
        bot_typing(user)
        create_photo_matrix(json_response["routes"])
        send_photo(user, "out.jpg", message)
        return json_response["routes"]


def write_msg(user, message, emoji):
    bot_typing(user)
    message = message.replace(" ", chr(32)) + emoji[random.randint(0, len(emoji) - 1)]
    vk.method('messages.send', {'user_id': user[0], 'message': message, 'random_id': user[1]})


def bot_typing(user):
    vk.method("messages.setActivity", {"type": "typing", "peer_id": user[0], "random_id": user[1]})
    

def send_photo(user, route, message):
    a = vk.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open(route, 'rb')}).json()
    c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    vk.method("messages.send", {"peer_id": user[0], "message": message, "attachment": f'photo{c["owner_id"]}_{c["id"]}',
                                'random_id': random.randint(100000000, 900000000)})


def random_search(user, message):
    bot_typing(user)
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "random"})
    json_response = response.json()
    send_photo(user, json_response["route"], message)


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
last_message = ""

for key in activators:
    list_of_commands.append(Commands(activators[key], list(map(add_person, answers[key]))))
    commands.extend(activators[key])

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

print("Бот запущен")

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                user = [event.user_id, random.randint(100000000, 900000000)]
                if event.type == VkEventType.USER_RECORDING_VOICE:
                    print("(Голосовое сообщение)")
                message = event.text
                hash_tag = False
                if "#" in message:
                    routes_list = tag_search(user, message, emoji)
                    hash_tag = True
                    if len(routes_list) > 0:
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    numbers = event.text.split()
                                    for number in numbers:
                                        if number.isdigit() and int(number) <= len(routes_list):
                                            send_photo(user, routes_list[int(number) - 1], "Фото")
                                    break
                message = analyze_text(message.lower().replace(' ', ''), commands)
                if message == last_message and not hash_tag:
                    write_msg(user, add_person(random_last_message()), emoji)
                elif message == "случайно":
                    random_search(user, message)
                elif message == "Nope" and not hash_tag:
                    write_msg(user, add_person(random_reiteration_message()), emoji)
                elif not hash_tag:
                    last_message = message
                    write_msg(user, find_command(message, list_of_commands), emoji)

