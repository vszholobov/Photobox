import os
import secrets
import copy
from PIL import Image
from flask_server import app


def code_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    return picture_fn


def save_picture(form_picture, picture_fn, path="static/profile_pictures"):
    """
    Сохраняет фотографии под случайным 16-значным именем в static/profile_pictures. Будет добавлена возможность
    сохранения фотографии в личную папку пользователя.

    Возвращает имя фотографии.
    """
    picture_path_1 = os.path.join(app.root_path, path + "images/", picture_fn)
    picture_path_2 = os.path.join(app.root_path, path + "scaled_images/", picture_fn)

    output_size = (500, 500)

    scaled_image = Image.open(form_picture)
    scaled_image.thumbnail(output_size)

    image = Image.open(form_picture)

    image.save(picture_path_1)
    scaled_image.save(picture_path_2)

    return picture_fn


def tags(string, tags=None):
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
    description = description.split()
    description.extend(tags)
    description = list(set(description))
    return description


def sort_pictures_by_tag(list_of_pictures, list_of_tags):
    """
    Сортирует фотографии по тегам, выбраным пользователем.

    Возвращает отсортированный по количеству совпадений список фотографий
    """

    count_of_coincidence = 0
    dict_of_pictures = {}
    sorted_list_of_pictures = []

    for picture in list_of_pictures:

        list_of_tags_of_picture = picture.tag_list

        for tag in list_of_tags_of_picture:
            if tag in list_of_tags:
                count_of_coincidence += 1

        if count_of_coincidence > 0:
            dict_of_pictures[picture.id] = count_of_coincidence

        count_of_coincidence = 0

    for coincidences in sorted(dict_of_pictures.items(), key=lambda item: item[1]):
        sorted_list_of_pictures.append(coincidences[0])

    return sorted_list_of_pictures


def sorting_tags_by_alphabet(tag_list):
    """
    Сортирует теги по алфавиту.

    Возвращает отсортированный по алфавиту список тегов.
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
