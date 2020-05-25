from os import getcwd
from PIL import Image, ImageFilter


def bright(source_name, brightness):
    """
    Функция, изменяющая яркость изображения.

    :param source_name: объект фотографии.
    :param brightness: уровень яркости.
    :return: обработанная фотография.
    """
    result = Image.new('RGB', source_name.size)
    for x in range(source_name.size[0]):
        for y in range(source_name.size[1]):
            r, g, b = source_name.getpixel((x, y))
            red = int(r * brightness)
            red = min(255, max(0, red))
            green = int(g * brightness)
            green = min(255, max(0, green))
            blue = int(b * brightness)
            blue = min(255, max(0, blue))
            result.putpixel((x, y), (red, green, blue))
    return result


def negative(source_name):
    """
    Функция, применяющая фильтр "Негатив" к изображению.

    :param source_name: объект фотографии.
    :return: обработанная фотография.
    """
    result = Image.new('RGB', source_name.size)
    for x in range(source_name.size[0]):
        for y in range(source_name.size[1]):
            r, g, b = source_name.getpixel((x, y))
            result.putpixel((x, y), (255 - r, 255 - g, 255 - b))
    return result


def white_black(source_name, brightness=1.2):
    """
    Функция, применяющая чёрно-белый фильтр к изображению.

    :param source_name: объект фотографии.
    :param brightness: уровень яркости.
    :return: обработанная фотография.
    """
    result = Image.new('RGB', source_name.size)
    separator = 255 / brightness / 2 * 3
    for x in range(source_name.size[0]):
        for y in range(source_name.size[1]):
            r, g, b = source_name.getpixel((x, y))
            total = r + g + b
            if total > separator:
                result.putpixel((x, y), (255, 255, 255))
            else:
                result.putpixel((x, y), (0, 0, 0))
    return result


def gray_scale(source_name):
    """
    Функция, применяющая фильтр "Оттенки серого".

    :param source_name: объект фотографии.
    :return: обработанная фотография.
    """
    result = Image.new('RGB', source_name.size)
    for x in range(source_name.size[0]):
        for y in range(source_name.size[1]):
            r, g, b = source_name.getpixel((x, y))
            gray = int(r * 0.2126 + g * 0.7152 + b * 0.0722)
            result.putpixel((x, y), (gray, gray, gray))
    return result


def sepia(source_name):
    """
    Функция, применяющая фильтр "Сепия".

    :param source_name: объект фотографии.
    :return: обработанная фотография.
    """
    result = Image.new('RGB', source_name.size)
    for x in range(source_name.size[0]):
        for y in range(source_name.size[1]):
            r, g, b = source_name.getpixel((x, y))
            red = int(r * 0.393 + g * 0.769 + b * 0.189)
            green = int(r * 0.349 + g * 0.686 + b * 0.168)
            blue = int(r * 0.272 + g * 0.534 + b * 0.131)
            result.putpixel((x, y), (red, green, blue))
    return result


def contrast(source_name, coefficient):
    """
    Функция, изменяющая контрастность изображения.

    :param source_name: объект фотографии.
    :param coefficient: уровень контрастности.
    :return: обработанная фотография.
    """
    result = Image.new('RGB', source_name.size)
    avg = 0
    for x in range(source_name.size[0]):
        for y in range(source_name.size[1]):
            r, g, b = source_name.getpixel((x, y))
            avg += r * 0.299 + g * 0.587 + b * 0.114
    avg /= source_name.size[0] * source_name.size[1]
    palette = []
    for i in range(256):
        temp = int(avg + coefficient * (i - avg))
        if temp < 0:
            temp = 0
        elif temp > 255:
            temp = 255
        palette.append(temp)
    for x in range(source_name.size[0]):
        for y in range(source_name.size[1]):
            r, g, b = source_name.getpixel((x, y))
            result.putpixel((x, y), (palette[r], palette[g], palette[b]))
    return result


def photo_filter(name_of_image, filter_name="contour"):
    """
    Функция выбора фильтра.

    :param name_of_image: объект фотографии.
    :param filter_name: название накладываемого фильтра.
    :return: обработанная фотография.
    """
    name_of_image = getcwd() + "/" + name_of_image
    image = Image.open(name_of_image)
    if filter_name == "contour":
        image = image.filter(ImageFilter.CONTOUR)
    elif filter_name == "detail":
        image = image.filter(ImageFilter.DETAIL)
    elif filter_name == "find_edges":
        image = image.filter(ImageFilter.FIND_EDGES)
    elif filter_name == "edge_enhance_more":
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
    elif filter_name == "edge_enhance":
        image = image.filter(ImageFilter.EDGE_ENHANCE)
    elif filter_name == "blur":
        image= image.filter(ImageFilter.BLUR)
    elif filter_name == "emboss":
        image = image.filter(ImageFilter.EMBOSS)
    elif filter_name == "sharpen":
        image = image.filter(ImageFilter.SHARPEN)
    elif filter_name == "smooth":
        image = image.filter(ImageFilter.SMOOTH)
    elif filter_name == "sepia":
        image = sepia(image)
    elif filter_name == "negative":
        image = negative(image)
    elif filter_name == "gray_scale":
        image = gray_scale(image)
    elif filter_name == "white_black":
        image = white_black(image)
    return image
