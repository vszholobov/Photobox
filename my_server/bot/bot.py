import vk_api
import random
import requests
from vk_api.longpoll import VkLongPoll, VkEventType

 
def write_msg(rand_int, user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': rand_int})


def bot_typing(rand_int, user_id):
    vk.method("messages.setActivity", {"type": "typing", "peer_id": user_id, "random_id": rand_int})
    

def photo_random(user_id, rand_int, route, message):
    a = vk.method("photos.getMessagesUploadServer")
    b = requests.post(a['upload_url'], files={'photo': open(route, 'rb')}).json()
    c = vk.method('photos.saveMessagesPhoto', {'photo': b['photo'], 'server': b['server'], 'hash': b['hash']})[0]
    vk.method("messages.send", {"peer_id": user_id, "message": message, "attachment": f'photo{c["owner_id"]}_{c["id"]}',
                                'random_id': rand_int})


def text_analize_bot(text):
    d = {}
    lenstr1 = len(text)
    commands = ["привет", "пока", "здравствуйте", "как дела?", "кто ты?", "время",
                "cколько времени?", "скажи", "случайно", "клоун", "прощай", "сайт",
                "икит", "погода"]
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


def add_person(string):
    return string + ", человек" + random.choice([".", "!"])


token = "845b43c4cd5c2b81f14efc3d0e878581dd6245acba70292db1c9a55d0d76fe252207e10f1842b8bcf40da"
good_bye = list(map(add_person, ['Пока', 'Аривидерчи', 'Гуд бай', 'До свидания', 'Покеда']))
hel_lo = list(map(add_person, ["Привет", "Х-а-а-а-й", "Здравствуй", "Гутен таг", "Дратути"]))
emoji = [" &#128526;", " &#129313;", " &#128108;", " &#128522;", " &#128515;", " &#128521;", " &#128518;", " &#128373;",
             " &#129314;", " &#128529;", " &#128567;", " &#128519;", " &#127482;&#127462;", " &#127465;&#127466;",
             " &#128169;"]
space = chr(32)

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

print("Бот запущен")

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                if event.type == VkEventType.USER_RECORDING_VOICE:
                    print("(Голосовое сообщение)")
                request = event.text
                randint = random.randint(100000000, 900000000)
                if request == "" or len(request) < 3:
                    request = "qwerty"
                elif request[0] != "#":
                    request = text_analize_bot(request.lower())
                if request == "привет" or request == "здравствуйте":
                    write_msg(randint, event.user_id, random.choice(hel_lo).replace(" ", space) + emoji[random.randint(0, 14)])
                elif request == "qwerty":
                    write_msg(randint, event.user_id, "Зачем мне это, человек?" + emoji[random.randint(0, 14)])
                elif request == "время" or request == "cколько времени?":
                    write_msg(randint, event.user_id, "Время?".replace(" ", space) + emoji[random.randint(0, 14)])
                elif request == "скажи":
                    write_msg(randint, event.user_id, "Не скажу, человек.".replace(" ", space) + emoji[random.randint(0, 14)])
                elif request == "клоун":
                    write_msg(randint, event.user_id, "&#129313;")
                elif request == "как дела?":
                    write_msg(randint, event.user_id, "Положительно. Но мое мнение может поменяться, "
                                                      "человек.".replace(" ", space) + emoji[random.randint(0, 14)])
                elif request == "пока" or request == "прощай":
                    write_msg(randint, event.user_id, random.choice(good_bye).replace(" ", space) + emoji[random.randint(0, 14)])
                elif request == "сайт":
                    write_msg(randint, event.user_id, "http://photobox.pythonanywhere.com/".replace(" ", space) + emoji[random.randint(0, 14)])
                elif request == "икит":
                    write_msg(randint, event.user_id, "Мой дом, человек!".replace(" ", space) + emoji[random.randint(0, 14)])
                elif request == "погода":
                    write_msg(randint, event.user_id, "Я не чувствую тела, я робот, человек!".replace(" ", space) + emoji[random.randint(0, 14)])
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
                else:
                    write_msg(randint, event.user_id, "Я не могу это расшифровать, прости.".replace(" ", space) + emoji[random.randint(0, 14)])


#data['object']['attachments'][0]
# chat_id = vk.method('messages.getConversations')
# chat_id = chat_id['items']
