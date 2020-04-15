import vk_api
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType


class Commands:
    def __init__(self, activators, answers):
        self.activators = activators
        self.answers = answers

    def check_command(self, command):
        return command in self.activators

    def return_random_answer(self):
        return random.choice(self.answers)


def find_command(text_of_command, list_of_commands):
    copy = list_of_commands.copy()
    for command in copy:
        if command.check_command(text_of_command):
            return command.return_random_answer()

 
def write_msg(user, message, emoji):
    bot_typing(user)
    message = message.replace(" ", chr(32)) + emoji[random.randint(0, len(emoji) - 1)]
    vk.method('messages.send', {'user_id': user[0], 'message': message, 'random_id': user[1]})


def bot_typing(user):
    vk.method("messages.setActivity", {"type": "typing", "peer_id": user[0], "random_id": user[1]})
    

def photo_random(user, route, message):
    a = vk.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open(route, 'rb')}).json()
    c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    vk.method("messages.send", {"peer_id": user[0], "message": message, "attachment": f'photo{c["owner_id"]}_{c["id"]}',
                                'random_id': random.randint(100000000, 900000000)})


def text_analize_bot(text, commands):
    d = {}
    lenstr1 = len(text)
    difference = []
    for command in commands:
        lenstr2 = len(command)
        for i in range(-1, lenstr1 + 1):
            d[(i, -1)] = i + 1
        for j in range(-1, lenstr2 + 1):
            d[(-1, j)] = j + 1
        for i in range(lenstr1):
            for j in range(lenstr2):
                if text[i] == command[j]:
                    cost = 0
                else:
                    cost = 1
                d[(i, j)] = min(
                    d[(i - 1, j)] + 1,
                    d[(i, j - 1)] + 1,
                    d[(i - 1, j - 1)] + cost,
                )
                if i and j and text[i] == command[j - 1] and text[i - 1] == command[j]:
                    d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)
        difference.append(d[lenstr1 - 1, lenstr2 - 1])
    print(difference)
    d = []
    dif = 0
    local_min = min(difference)
    for i in range(len(difference)):
        if difference[i] == local_min:
            difference[i] = dif - 1
            dif -= 1
            d.append(commands[difference.index(min(difference))])
    print(d)
    for i in range(len(d)):
        print(str_analise_bot(d[i], text))
        d[i] = str_analise_bot(d[i], text)
    print(d)
    return random.choice(d)


def add_person(string):
    return string + ", человек" + random.choice([".", "!"])


def hashtag_search(user, message, emoji):
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "tags", "tags": message})
    json_response = response.json()
    if len(json_response["routes"]) < 1:
        write_msg(user, "Ничего не нашёл, человек", emoji)
    else:
        for i in range(len(json_response["routes"])):
            bot_typing(user)
            photo_random(user, json_response["routes"][i], message)


def random_search(user, message):
    bot_typing(user)
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "random"})
    json_response = response.json()
    photo_random(user, json_response["route"], message)


def random_last_message():
    message = ["Ты повторился", "Опять", "Вроде не смешно", "Повторение", "Я почему-то вижу эхо", "Отзвук"]
    return random.choice(message)


def random_reiteration_message():
    message = ["Не смог распознать", "Анализ произошел неудачно", "Знаю тысячи языков, но это не смог распознать",
               "Сложные буквы"]
    return random.choice(message)


def str_analise_bot(str1, str2):
    similarity = 0
    max_str_len = min(len(str1), len(str2))
    for i in range(max_str_len):
        if str1[i] == str2[i]:
            similarity += 1
    residual = max_str_len/2
    if similarity > residual:
        return str1
    else:
        return "Nope"


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
                if "#" in message:
                    hashtag_search(user, message, emoji)
                message = text_analize_bot(message.lower().replace(' ', ''), commands)
                if message == last_message:
                    write_msg(user, add_person(random_last_message()), emoji)
                elif message == "случайно":
                    random_search(user, message)
                elif message == "Nope":
                    write_msg(user, add_person(random_reiteration_message()), emoji)
                else:
                    last_message = message
                    write_msg(user, find_command(message, list_of_commands), emoji)


#data['object']['attachments'][0]
# chat_id = vk.method('messages.getConversations')
# chat_id = chat_id['items']


"""

                elif request == "случайно":
                    bot_typing(random.randint(100000000, 900000000), event.user_id)
                    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "random"})
                    json_response = response.json()
                    photo_random(event.user_id, randint, json_response["route"], request)
                elif request[0] == "#":
                    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "tags",
                                                                                "tags": request})
                    json_response = response.json()
                    if len(json_response["routes"]) < 1:
                        write_msg(randint, event.user_id, "Ничего не нашёл, человек!".replace(" ", space))
                    else:
                        for i in range(len(json_response["routes"])):
                            bot_typing(random.randint(100000000, 900000000), event.user_id)
                            photo_random(event.user_id, random.randint(100000000, 900000000),
                                         json_response["routes"][i], request.replace(' ', ''))

"""

"""
commands = ["привет", "пока", "здравствуйте", "как дела?", "кто ты?", "время",
                "cколько времени?", "скажи", "случайно", "клоун", "прощай", "сайт",
                "икит", "погода"]
                
                def text_analize_bot(text, commands):
    d = {}
    lenstr1 = len(text)
    difference = []
    for command in commands:
        lenstr2 = len(command)
        for i in range(-1, lenstr1 + 1):
            d[(i, -1)] = i + 1
        for j in range(-1, lenstr2 + 1):
            d[(-1, j)] = j + 1
        for i in range(lenstr1):
            for j in range(lenstr2):
                if text[i] == command[j]:
                    cost = 0
                else:
                    cost = 1
                d[(i, j)] = min(
                    d[(i - 1, j)] + 1,
                    d[(i, j - 1)] + 1,
                    d[(i - 1, j - 1)] + cost,
                )
                if i and j and text[i] == command[j - 1] and text[i - 1] == command[j]:
                    d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)
        difference.append(d[lenstr1 - 1, lenstr2 - 1])
    print(difference)
    a = difference.index(min(difference))
    difference = commands[difference.index(min(difference))]
    return difference
"""
