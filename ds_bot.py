import datetime

import discord
import wikipedia
from discord.ext import commands

import config

prefix = '%'
client = commands.Bot(command_prefix=prefix)


@client.event
async def on_message(message):
    words = message.content.split()
    important_words = ' '.join(words[1:])
    if message.content.startswith(f'{prefix}s'):
        search = discord.Embed(title='Successful search...', description=wiki_summary(important_words),
                               color=discord.Color.purple())
        await message.channel.send(content=None, embed=search)
        return
    await client.process_commands(message)


@client.command(name='lang')
async def set_lang(context: commands.context.Context):
    words = context.message.content.split()
    lang = ' '.join(words[1:])
    wikipedia.set_lang(prefix=lang)
    msg = discord.Embed(title='Language changed', description=f'Language is {lang}',
                        color=discord.Color.red())
    await context.channel.send(content=None, embed=msg)


@client.event
async def on_ready():
    time = datetime.datetime.now()
    print('WikiBot online at {}'.format(time))


def wiki_summary(arg):
    definition = wikipedia.summary(arg, sentences=3, chars=1000,
                                   auto_suggest=True, redirect=True)
    return definition


client.run(config.token)
