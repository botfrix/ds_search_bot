import datetime
import discord
import wikipedia
from discord.ext import commands
from config import token

wikipedia.set_lang('ru')

client = commands.Bot(command_prefix='@')

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
    if message.content.startswith('@se'):
        words = message.content.split()
        important_words = ' '.join(words[1:])
        search = discord.Embed(title='Successful search...', description=wiki_summary(important_words),
                               color=discord.Color.purple())
        await message.channel.send(content=None, embed=search)

client.run(token)

