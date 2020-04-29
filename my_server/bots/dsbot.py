import discord
from discord.ext import commands
from bot_functions import create_photo_matrix
import requests

bot = commands.Bot(command_prefix='pb!')


@bot.event
async def on_ready():
    print("Бот запущен")
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)


def random_search():
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "random"})
    json_response = response.json()
    return json_response["route"]


def tag_search(message):
    response = requests.post("http://127.0.0.1:5000/bot", json={"action": "tags", "tags": message})
    json_response = response.json()
    if len(json_response["routes"]) < 1:
        return False
    else:
        create_photo_matrix(json_response["routes"])
        return True


@bot.command()
async def random(ctx):
    await ctx.send(file=discord.File(random_search()))


@bot.command()
async def search(ctx, tags: str):
    if not tag_search(tags):
        await ctx.send("Not found")
    else:
        await ctx.send(file=discord.File("out.jpg"))

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


    
bot.run('NzA0NTk2OTQzMTQ5NzI3Nzc0.XqgWWQ.gAvXH6C3Ex5sqaR9lfI8AL2heZ8')
