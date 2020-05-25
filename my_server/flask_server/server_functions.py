import os
import secrets
import copy
from PIL import Image
from flask_server import app
from datetime import datetime


def creation_date(date=datetime.now()):
    """
    Функция возвращает дату для фотографии при сохранении.
    :param date: текущая дата
    :return: дата в виде "25 Мая 2020".
    """
    month = {1: "января", 2: "февраля",
             3: "марта", 4: "апреля",
             5: "мая", 6: "июня",
             7: "июля", 8: "августа",
             9: "сентября", 10: "октября",
             11: "ноября", 12: "декабря"}

    date = date.strftime(f"%d {month[int(date.strftime('%m'))]} 20%y").split()

    return date[0] + " " + date[1].capitalize() + " " + date[2]


def code_picture(form_picture):
    """
    Функция задает имя фотографии в закодираванном виде.

    :param form_picture: объект фотографии.
    :return: закодираванное имя фотографии.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    return picture_fn


def size_t_analise(image):
    """
    Функция определяет размер фотографии, исходя из соотношения её сторон.
    :param image: объект фотографии.
    :return: размер фотографии в виде кортежа.
    """
    size = image.size
    if (size[0] / size[1]) >= 1.2:
        shape = (300, 150)
    elif (size[0] / size[1]) <= 0.8:
        shape = (150, 300)
    else:
        shape = (150, 150)
    return shape


def size_analise(image):
    """
    Функция обрезает фотографию, делая из нее квадрат со стороной равной длине меньшей стороны изначальной фотографии,
    при этом центрируя новую фотографию относительно исходной.

    :param image: объект фотографии.
    :return: измененный обьект переданной фотографии.
    """
    # size[0] - длина(горизонт)
    size = image.size

    # width = size[0]
    # height = size[1]

    if size[0] > size[1]:
        distance = (size[0] - size[1])/2
        image = image.crop((distance, 0, size[0] - distance, size[1])) # im.crop((left, top, right, bottom))
    elif size[0] < size[1]:
        distance = (size[1] - size[0]) / 2
        image = image.crop((0, distance, size[0], size[1] - distance))
    return image


def save_picture(form_picture, picture_fn, path="static/profile_pictures"):
    """
    Сохраняет фотографии под случайным 16-значным именем в static/profile_pictures.

    :param form_picture: объект фотографии
    :param picture_fn: имя фотографии
    :param path: директория для сохранения фотографий.
    :return: возвращает отношение высоты к ширине фотографии.
    """

    try:
        image = Image.open(form_picture)
        htwRatio = image.size[1] / image.size[0]
        if htwRatio > 2.5:
            return False
        if len(image.fp.read()) > 3145728:
            return False
    except Exception:
        return False
    if path == "static/profile_pictures":

        picture_path_3 = os.path.join(app.root_path, path, picture_fn)

        scaled_image = Image.open(form_picture)
        scaled_image = size_analise(scaled_image)
        scaled_image.save(picture_path_3)

        return picture_fn

    picture_path_1 = os.path.join(app.root_path, path + "images/", picture_fn)

    if image.format == "GIF":
        image.save(picture_path_1, save_all=True)
    else:
        image.save(picture_path_1)

    return htwRatio


def tags(string, tags=None):
    """
    Функция обнаруживает тэги в сообщении пользователя и добавляет их в tags.
    :param string: строка, которую ввел пользователь.
    :param tags: список тэгов фотографий.
    :return: обновленный список фотографий.
    """
    if tags is None:
        tags = []

    # Проверка на корректный ввод "#". Ловит строки типа "# # ", "##".
    check_string = string.replace(" ", "")
    for i in range(1, len(check_string)):
        if check_string[i] == check_string[i - 1] == "#":
            # Ошибка 1
            return tags

    string = string.strip(" ").rstrip("#")
    cnt = string.count("#")

    if not cnt:
        # Ошибка 2
        return tags

    # Обработка строки
    for i in range(cnt):

        # Разбиение на тэги
        pos1 = string.find("#")
        pos2 = string.find("#", pos1 + 1)
        if pos2 == -1:
            pos2 = len(string)

        tag = string[pos1:pos2 - pos1:1]
        tag = tag.strip().replace(" ", "_")

        # Замена кусков строки типа "____" на "_"
        i = 1
        length = len(tag)
        while i < length:
            if tag[i] == tag[i - 1] == "_":
                tag = tag[:i:] + tag[i + 1::1]
                i -= 1
                length -= 1
            i += 1

        if not (tag in tags):
            tags.append(tag)
        string = string[pos2::1]
    return tags


def join_templates(tags, description):
    """
    Функция соединяет тэги и описание в один список.
    :param tags: список тэгов.
    :param description: описание фотографии.
    :return: список из тэгов и описания.
    """
    description = description.split()
    description.extend(tags)
    description = list(set(description))
    return description


def sort_pictures_by_tag(list_of_pictures, list_of_tags):
    """
    Сортирует фотографии по тегам, выбраным пользователем.

    :param list_of_pictures: список объектов фотографий.
    :param list_of_tags: список тэгов.
    :return: возвращает кортеж, состоящий из списка директорий и списка индентификаторов пользователей.
    """

    count_of_coincidence = 0
    dict_of_pictures = {}
    sorted_list_of_pictures = []
    sorted_list_of_ids = []

    for picture in list_of_pictures:

        list_of_tags_of_picture = picture.tag_list

        for tag in list_of_tags_of_picture:
            if tag in list_of_tags:
                count_of_coincidence += 1

        if count_of_coincidence > 0:
            dict_of_pictures[picture] = count_of_coincidence

        count_of_coincidence = 0

    for coincidences in sorted(dict_of_pictures.items(), key=lambda item: item[1]):
        sorted_list_of_pictures.append(coincidences[0].image_file)
        sorted_list_of_ids.append(coincidences[0].user_id)

    return sorted_list_of_pictures, sorted_list_of_ids


def sorting_tags_by_alphabet(tag_list):
    """
    Сортирует теги по алфавиту.

    :param tag_list: cписок тэгов.
    :return: Возвращает отсортированный по алфавиту список тегов.
    """

    # Ё = 1025
    # А = 1040   Я = 1071
    # ё = 1105
    # а = 1072   я = 1103

    # A = 65 Z = 90
    # a = 97 z = 122

    tag_list = copy.deepcopy(tag_list)
    working_dict = {}
    count_of_e = 0
    dict_of_rus_alphabet = {}
    dict_of_eng_alphabet = {}
    dict_of_symbols = {}
    sorted_tag_list = []

    for tag in tag_list:
        if (tag.count("Ё") + tag.count("ё") + tag.count("Е") + tag.count("е")) >= count_of_e:
            count_of_e = tag.count("Ё") + tag.count("ё") + tag.count("Е") + tag.count("е")

    for tag in tag_list:

        if ("Е" in tag or
            "е" in tag or
            "Ё" in tag or
                "ё" in tag):
            tag_changed = tag.replace("е", "е0").replace("Е", "Е0")
            tag_changed = tag_changed.replace("ё", "е1").replace("Ё", "Е1")
            working_dict[tag] = tag_changed

        else:
            tag_changed = tag + count_of_e * " "
            working_dict[tag] = tag_changed

    for tag in working_dict.items():

        if (1040 <= ord(tag[1][1]) <= 1103 or
                ord(tag[1][1]) == 1105 or
                ord(tag[1][1]) == 1025):
            dict_of_rus_alphabet[tag[0]] = tag[1]

        elif (65 <= ord(tag[1][1]) <= 90 or
              97 <= ord(tag[1][1]) <= 122):
            dict_of_eng_alphabet[tag[0]] = tag[1]

        else:
            dict_of_symbols[tag[0]] = tag[1]

    dict_of_eng_alphabet = dict(sorted(dict_of_eng_alphabet.items(), key=lambda item: item[1]))
    for tag in dict_of_eng_alphabet:
        sorted_tag_list.append(tag)

    dict_of_rus_alphabet = dict(sorted(dict_of_rus_alphabet.items(), key=lambda item: item[1]))
    for tag in dict_of_rus_alphabet:
        sorted_tag_list.append(tag)

    dict_of_symbols = dict(sorted(dict_of_symbols.items(), key=lambda item: item[1]))
    for tag in dict_of_symbols:
        sorted_tag_list.append(tag)

    return sorted_tag_list


def creating_routes(list_of_images):
    """
    Функция заполняет у объекта фотографий атрибут route.
    :param list_of_images: список объектов фотографий.
    """
    for image in list_of_images:
        image.route = '/users/' + str(image.user_id) + '/scaled_images/' + str(image.image_file)

