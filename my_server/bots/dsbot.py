import discord
from discord.ext import commands
from bot_functions import create_photo_matrix
import requests

bot = commands.Bot(command_prefix='pb!')


@bot.event
async def on_ready():
    """
    Функция показывает программисту запуск бота.
    """
    print("Бот запущен")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)


def random_search():
    """
    Функция делает запрос на сервер и отправляет случайную фотографию.

    :return: директорию случайной фотографии.
    """
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "random"})
    json_response = response.json()
    return json_response["route"]


def tag_search(message):
    """
    Функция делает запрос на сервер и создает матрицу фотографий.

    :param message: сообщение от пользователя.
    :return: Наличие фотографий.
    """
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "tags", "tags": message})
    json_response = response.json()
    if len(json_response["routes"]) < 1:
        return False
    else:
        create_photo_matrix(json_response["routes"])
        return True


@bot.command()
async def random(ctx):
    """
    Функция отправляет случайную фотографию в группу.

    :param ctx: объект бота.
    """
    await ctx.send(file=discord.File(random_search()))


@bot.command()
async def search(ctx, tags: str):
    """
    Функция отправляет фотографию пользователям в группу.

    :param ctx: объект бота.
    :param tags: сообщение с тэгами от пользователя.
    """
    if not tag_search(tags):
        await ctx.send("Not found")
    else:
        await ctx.send(file=discord.File("out.jpg"))


@bot.command()
async def test(ctx, arg):
    """
    Функция возвращает пользователю в группу его же сообщение.

    :param ctx: объект бота.
    :param arg: сообщение пользователя.
    """
    await ctx.send(arg)


    
bot.run('NzA0NTk2OTQzMTQ5NzI3Nzc0.XqgWWQ.gAvXH6C3Ex5sqaR9lfI8AL2heZ8')
