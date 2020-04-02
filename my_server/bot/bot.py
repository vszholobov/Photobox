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


token = "a003e074b079bb141039a77c63597331c9779be8e57c5a718e465f95a277fa6e66829e6d17ffe8227e042"
space = chr(32)

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

print("Бот запущен")

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                randint = random.randint(100000000, 900000000)
                if request[0] != "#":
                    request = request.lower()
                chat_id = vk.method('messages.getConversations')
                chat_id = chat_id['items']
                if request == "привет":
                    write_msg(randint, event.user_id, "Привет, Человек!".replace(" ", space))
                elif request == "2":
                    write_msg(randint, event.user_id, "&#129313;")
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
                    write_msg(randint, event.user_id, "Я не могу это расшифровать, прости.".replace(" ", space))
