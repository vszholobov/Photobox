import vk_api
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
import bot_functions
import json
import os


def tag_search(user, message, emoji, keyboard):
    """
    Функция по тэгам ищет фотографии: делает запрос на сервер и возвражает директории фотографий.

    :param user: кортеж из индентификатора и случайного числа в виде кортежа.
    :param message: сообщение для пользователя.
    :param emoji: список эмодзи.
    :param keyboard: клавиатура в виде словаря.
    :return: список директорий фотографий.
    """
    bot_typing(user)
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "tags", "tags": message})
    json_response = response.json()
    if len(json_response["routes"]) < 1:
        write_msg(user, "Ничего не нашёл, человек", emoji, keyboard)
        return []
    elif len(json_response["routes"]) == 1:
        send_photo(user, json_response["routes"][0], message)
        return json_response["routes"]
    else:
        bot_functions.create_photo_matrix(json_response["routes"], user[0])
        send_photo(user, str(user[0]) + ".jpg", message)
        return json_response["routes"]


def write_msg(user, message, emoji, keyboard):
    """
    Функция отправляет сообщение пользователя через бота.

    :param user: кортеж из индентификатора и случайного числа.
    :param message: сообщение для пользователя.
    :param emoji: список эмодзи.
    :param keyboard: клавиатура в виде словаря.
    """
    bot_typing(user)
    user[1] = random.randint(100000000, 900000000)
    message = message.replace(" ", chr(32)) + emoji[random.randint(0, len(emoji) - 1)]
    vk.method('messages.send', {'user_id': user[0], 'message': message, 'random_id': user[1], "keyboard": keyboard})


def bot_typing(user):
    """
    Функция, имитирующая печатание сообщение бота при общении с пользователем.

    :param user: кортеж из индентификатора и случайного числа.
    """
    vk.method("messages.setActivity", {"type": "typing", "peer_id": user[0], "random_id": user[1]})
    

def send_photo(user, route, message):
    """
    Функция, обеспечивающая боту отправление фотографий пользователю.

    :param user: кортеж из индентификатора и случайного числа в виде кортежа.
    :param message: сообщение для пользователя.
    :param route: директория фотографии.
    """
    a = vk.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open(route, 'rb')}).json()
    c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    vk.method("messages.send", {"peer_id": user[0], "message": message, "attachment": f'photo{c["owner_id"]}_{c["id"]}',
                                'random_id': random.randint(100000000, 900000000)})


def random_search(user, message):
    """
    Функция делает запрос на сервер и затем отправляет случайную фотографию пользователю.

    :param user: кортеж из индентификатора и случайного числа в виде кортежа.
    :param message: сообщение для пользователя.
    """
    bot_typing(user)
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "random"})
    json_response = response.json()
    send_photo(user, json_response["route"], message)


list_of_commands = []
commands = []
last_message = None

for key in bot_functions.activators:
    list_of_commands.append(bot_functions.Commands(bot_functions.activators[key],
                                                   list(map(bot_functions.add_person,
                                                        bot_functions.answers[key]))))
    commands.extend(bot_functions.activators[key])

keyboard = {
    "one_time": False,
    "buttons": [
        [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Случайно"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": [],
                    "label": "Команды"
                },
                "color": "positive"
        }]
    ]
}

if __name__ == '__main__':
    vk = vk_api.VkApi(token=bot_functions.vk_token)
    longpoll = VkLongPoll(vk)
    keyboard = str(json.dumps(keyboard, ensure_ascii=False))

    print("Бот запущен")

    while True:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                user = [event.user_id, random.randint(100000000, 900000000)]
                if "#" in event.text:
                    routes_list = tag_search(user, event.text, bot_functions.vk_emoji, keyboard)
                    if len(routes_list) > 1:
                        write_msg(user, "Выберите цифры фотографий через пробел!", bot_functions.vk_emoji, keyboard)
                        for second_event in longpoll.listen():
                            if second_event.type == VkEventType.MESSAGE_NEW and second_event.to_me:
                                numbers = second_event.text.split()
                                numbers = list(set(numbers))
                                for number in numbers:
                                    if number.isdigit() and int(number) <= len(routes_list):
                                        send_photo(user, routes_list[int(number) - 1], event.text)
                                    else:
                                        print(1)
                                        write_msg(user, f"Выбора {number} нет.", bot_functions.vk_emoji, keyboard)
                                path = os.path.join(os.path.abspath(os.path.dirname(__file__)), str(user[0]) + '.jpg')
                                try:
                                    os.remove(path)
                                except OSError:
                                    print(f"~DELETION-ERROR: {path};")
                                break
                else:
                    message = bot_functions.analyze_text(event.text.lower().replace(' ', ''), commands)
                    if event.text == last_message and message != "случайно":
                        write_msg(user, bot_functions.add_person(bot_functions.random_last_message()),
                                  bot_functions.vk_emoji, keyboard)
                    elif message == "случайно":
                        random_search(user, message)
                    elif message == "Nope":
                        write_msg(user, bot_functions.add_person(bot_functions.random_nope_message()),
                                  bot_functions.vk_emoji, keyboard)
                    else:
                        write_msg(user, bot_functions.find_command(message, list_of_commands), bot_functions.vk_emoji,
                                  keyboard)
                    last_message = event.text
