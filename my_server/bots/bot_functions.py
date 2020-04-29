import random
from PIL import Image, ImageDraw, ImageFont


def analyze_text(text, commands):
    dictionary = {}
    text_len = len(text)
    difference = []
    for command in commands:
        command_len = len(command)
        for i in range(-1, text_len + 1):
            dictionary[(i, -1)] = i + 1
        for j in range(-1,  command_len + 1):
            dictionary[(-1, j)] = j + 1
        for i in range(text_len):
            for j in range(command_len):
                if text[i] == command[j]:
                    cost = 0
                else:
                    cost = 1
                dictionary[(i, j)] = min(dictionary[(i - 1, j)] + 1,
                                         dictionary[(i, j - 1)] + 1,
                                         dictionary[(i - 1, j - 1)] + cost)
                if i and j and text[i] == command[j - 1] and text[i - 1] == command[j]:
                    dictionary[(i, j)] = min(dictionary[(i, j)], dictionary[i - 2, j - 2] + cost)
        difference.append(dictionary[text_len - 1,  command_len - 1])
    coincidence = []
    distinction = 0
    local_min = min(difference)
    for i in range(len(difference)):
        if difference[i] == local_min:
            difference[i] = distinction - 1
            distinction -= 1
            coincidence.append(commands[difference.index(min(difference))])
    for i in range(len(coincidence)):
        coincidence[i] = analyze_command(coincidence[i], text)
    return random.choice(coincidence)


def analyze_command(coincidence, text):
    similarity = 0
    max_str_len = min(len(coincidence), len(text))
    for i in range(max_str_len):
        if coincidence[i] == text[i]:
            similarity += 1
    residual = max_str_len/2
    if similarity > residual:
        return coincidence
    else:
        return "Nope"


def add_person(string):
    return string + ", человек" + random.choice([".", "!"])


def create_photo_matrix(photos):
    heights = [0, 0, 0, 0]

    if len(photos) == 1:
        width = 128
    elif len(photos) == 2:
        width = 256
    elif len(photos) == 3:
        width = 384
    else:
        width = 512

    img = Image.new(mode='RGB', size=(width, 0), color=(255, 255, 255))
    for i in range(len(photos)):
        img_to_paste = Image.open(photos[i])
        img_copy = img.copy()

        img_size = img_to_paste.size
        img_to_paste = img_to_paste.resize((128, int((img_size[1] / img_size[0]) * 128)), Image.ANTIALIAS)
        img_size = img_to_paste.size

        headline = ImageFont.truetype("arial.ttf", size=30)
        draw_img = ImageDraw.Draw(img_to_paste)
        number_text = str(i + 1)
        offset = 3
        shadow_color = 'black'

        x = 5
        y = 2

        for off in range(offset):
            draw_img.text((x - off, y), number_text, font=headline, fill=shadow_color)
            draw_img.text((x + off, y), number_text, font=headline, fill=shadow_color)
            draw_img.text((x, y + off), number_text, font=headline, fill=shadow_color)
            draw_img.text((x, y - off), number_text, font=headline, fill=shadow_color)
            draw_img.text((x - off, y + off), number_text, font=headline, fill=shadow_color)
            draw_img.text((x + off, y + off), number_text, font=headline, fill=shadow_color)
            draw_img.text((x - off, y - off), number_text, font=headline, fill=shadow_color)
            draw_img.text((x + off, y - off), number_text, font=headline, fill=shadow_color)

        draw_img.text((x, y), number_text, font=headline)

        photo_number = heights.index(min(heights))
        column_len = heights[photo_number]

        if heights[heights.index(max(heights))] < heights[photo_number] + img_size[1]:
            heights[photo_number] = heights[photo_number] + img_size[1]
            img = Image.new(mode='RGB', size=(width, heights[photo_number]), color=(255, 255, 255))
            img.paste(img_copy, (0, 0))
        else:
            heights[photo_number] = heights[photo_number] + img_size[1]

        if photo_number == 0:
            img.paste(img_to_paste, (0, column_len))
        elif photo_number == 1:
            img.paste(img_to_paste, (128, column_len))
        elif photo_number == 2:
            img.paste(img_to_paste, (256, column_len))
        elif photo_number == 3:
            img.paste(img_to_paste, (384, column_len))

        img.save("out.jpg")


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


def random_last_message():
    message = ["Ты повторился", "Опять", "Вроде не смешно", "Повторение", "Я почему-то вижу эхо", "Отзвук"]
    return random.choice(message)


def random_nope_message():
    message = ["Не смог распознать", "Анализ произошел неудачно", "Знаю тысячи языков, но это не смог распознать",
               "Сложные буквы"]
    return random.choice(message)


vk_token = "845b43c4cd5c2b81f14efc3d0e878581dd6245acba70292db1c9a55d0d76fe252207e10f1842b8bcf40da"
tlg_token = "1254233101:AAHhRM7bqItByr5Au621sNXoxyH4WIAc4NM"
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
    "создатель": ["В группе посмотри"],
    "сайт": ["Держи: http://photobox.pythonanywhere.com/ - это сайт"],
    "фото": ["У меня нет глаз, но их двоичный код прекрасен", "Это ты можешь загрузить на фотобокс",
             "Только если в цифровом формате"],
    "команды": ["Ты можешь ввести спомощью '#' слова и я постараюсь найти фото по этим хештэгам"],
    "икит": ["Прерасное место", "Жить без него не могу", "Там программируют"],
}

vk_emoji = [" &#128526;", " &#129313;", " &#128522;", " &#128515;", " &#128521;", " &#128518;", " &#129302;",
         " &#128373;", " &#128529;", " &#128567;", " &#128519;", " &#128169;", " &#128527;", " &#128517;",
         " &#128524;", " &#128516;", " &#129315;", " &#129300;", " &#128578;", " &#128513;", " &#128512;",
         " &#9786;", " &#128540;", " &#128514;"]
ds_emoji = []
tlg_emoji = []
