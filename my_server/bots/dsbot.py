import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='')

@bot.command()
async def cat(ctx):
    await ctx.send(file=discord.File('C:\\Users\\user\\Desktop\\filter\\image.jpg'))
    
bot.run('NzA0NTk2OTQzMTQ5NzI3Nzc0.XqgWWQ.gAvXH6C3Ex5sqaR9lfI8AL2heZ8')
