import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import datetime
import random
from random import randint
import wikipedia

client = commands.Bot(command_prefix = '!')

owner_id = 383623196894822400
chan_id = 813544820991197197

token = ' '

@client.event
async def on_ready():
    time = datetime.datetime.now()
    print('WikiBot online at {}'.format(time))

def wiki_summary(arg):
    definition = wikipedia.summary(arg, sentences=3, chars=1000,
    auto_suggest=True, redirect=True)
    return definition

@client.event
async def on_message(message):
    words = message.content.split()
    important_words = words[1:]

    if message.content.startswith('!search'):
        words = message.content.split()
        important_words = words[1:]
        search = discord.Embed(title='Successful search...', description=wiki_summary(important_words), color=discord.Color.purple())
        await message.channel.send(content=None, embed=search)

client.run(token)