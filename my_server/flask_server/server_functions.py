import os
import secrets
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
    picture_path = os.path.join(app.root_path, path, picture_fn)

    output_size = (250, 250)
    scaled_image = Image.open(form_picture)
    scaled_image.thumbnail(output_size)

    scaled_image.save(picture_path)

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
