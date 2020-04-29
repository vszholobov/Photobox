import vk_api
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
import bot_functions


def tag_search(user, message, emoji):
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "tags", "tags": message})
    json_response = response.json()
    if len(json_response["routes"]) < 1:
        write_msg(user, "Ничего не нашёл, человек", emoji)
        return []
    elif len(json_response["routes"]) == 1:
        send_photo(user, json_response["routes"][0], message)
        return json_response["routes"]
    else:
        bot_typing(user)
        bot_functions.create_photo_matrix(json_response["routes"])
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


list_of_commands = []
commands = []
last_message = None

for key in bot_functions.activators:
    list_of_commands.append(bot_functions.Commands(bot_functions.activators[key],
                                                   list(map(bot_functions.add_person,
                                                        bot_functions.answers[key]))))
    commands.extend(bot_functions.activators[key])

vk = vk_api.VkApi(token=bot_functions.vk_token)
longpoll = VkLongPoll(vk)

print("Бот запущен")

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.USER_RECORDING_VOICE and event.to_me:
            user = [event.user_id, random.randint(100000000, 900000000)]
            print("(Голосовое сообщение)")
            write_msg(user, bot_functions.add_person("Не понимаю голосовых"), bot_functions.vk_emoji)
        elif event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user = [event.user_id, random.randint(100000000, 900000000)]
            if "#" in event.text:
                routes_list = tag_search(user, event.text, bot_functions.vk_emoji)
                if len(routes_list) > 1:
                    for second_event in longpoll.listen():
                        if second_event.type == VkEventType.MESSAGE_NEW and second_event.to_me:
                            numbers = second_event.text.split()
                            numbers = list(set(numbers))
                            for number in numbers:
                                if number.isdigit() and int(number) <= len(routes_list):
                                    send_photo(user, routes_list[int(number) - 1], event.text)
                                else:
                                    write_msg(user, f"Выбора {number} нет.",
                                              bot_functions.vk_emoji)
                            break
            else:
                message = bot_functions.analyze_text(event.text.lower().replace(' ', ''), commands)
                if event.text == last_message:
                    write_msg(user, bot_functions.add_person(bot_functions.random_last_message()),
                              bot_functions.vk_emoji)
                elif message == "случайно":
                    random_search(user, message)
                elif message == "Nope":
                    write_msg(user, bot_functions.add_person(bot_functions.random_nope_message()),
                              bot_functions.vk_emoji)
                else:
                    write_msg(user, bot_functions.find_command(message, list_of_commands), bot_functions.vk_emoji)
                last_message = event.text

