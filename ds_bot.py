import datetime

import discord
import wikipedia
from wikipedia import WikipediaPage
from discord.ext import commands

import config

prefix = '!'
client = commands.Bot(command_prefix=prefix)

client.remove_command('help')


@client.event
async def on_ready():
    time = datetime.datetime.now()
    print('WikiBot online at {}'.format(time))


def wiki_summary(arg):
    definition = wikipedia.summary(arg, sentences=3, chars=1000,
                                   auto_suggest=True, redirect=True)
    return definition


@client.command(name='s')
async def wiki_search(context: commands.context.Context):
    words = context.message.content.split()
    important_words = ' '.join(words[1:])
    if important_words == '':
        err = discord.Embed(title='Введите что-либо для поиска!',
                            description=None,
                            color=discord.Color.dark_red())
        await context.channel.send(content=None, embed=err)
    else:
        search = discord.Embed(title=f'Поиск по запросу {important_words}...',
                               description=wiki_summary(important_words),
                               color=discord.Color.purple())
        await context.channel.send(content=None, embed=search)


@client.command(name='lang')
async def set_lang(context: commands.context.Context):
    words = context.message.content.split()
    lang = ' '.join(words[1:])
    if lang == '':
        err = discord.Embed(title='Введите аббревиатуру языка!',
                            description=f'{prefix}help - для просмотра списка языков',
                            color=discord.Color.dark_red())
        await context.channel.send(content=None, embed=err)
    else:
        wikipedia.set_lang(prefix=lang)
        msg = discord.Embed(title='Язык изменён', description=f'Текущий язык: "{lang}"',
                            color=discord.Color.orange())
        await context.channel.send(content=None, embed=msg)


@client.command(name='help')
async def help(context: commands.context.Context):
    msg = discord.Embed(title='Список команд:',
                        description=f'{prefix}help - вызвать список команд\n\n'
                                    f'{prefix}s - поиск по запросу\n\n'
                                    f'{prefix}lang - смена языка поиска:\nru - русский'
                                    '\nen - английский\nfr - французский'
                                    '\nde - немецкий\nit - итальянский'
                                    '\nes - испанский\nzh - китайский'
                                    '\nja - японский\nar - арабский'
                                    '\nuk - украинский\n',
                        color=discord.Color.orange())
    await context.channel.send(content=None, embed=msg)


client.run(config.token)
