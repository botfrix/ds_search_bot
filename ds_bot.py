import json
import datetime

import discord
import wikipedia
from discord.ext import commands

import config

from my_json_encoder import MyEncoder, Message

data = {"messages": []}
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


@client.event
async def on_message(message):
    split_message = message.content.split()
    if len(split_message) == 0:
        return
    tag = split_message[0]
    msg = Message(tag, message.author, message.content)
    data["messages"].append(msg)
    await client.process_commands(message)


@client.event
async def on_disconnect():
    time = datetime.datetime.now()
    print('WikiBot offline at {}'.format(time))
    with open ('users_data.json', 'w') as file:
        json.dump(data, file, cls=MyEncoder, indent=4)


@client.command(name='stop')
@commands.is_owner()
async def bot_shutdown(ctx):
    await ctx.bot.logout()


@client.command(name='s')
async def wiki_search(context: commands.context.Context):
    words = context.message.content.split()
    important_words = ' '.join(words[1:])
    if important_words == '':
        err = discord.Embed(title='Enter something to search!',
                            description=None,
                            color=discord.Color.dark_red())
        await context.channel.send(content=None, embed=err)
    else:
        search = discord.Embed(title=f'Searching for {important_words}...',
                               description=wiki_summary(important_words),
                               color=discord.Color.purple())
        await context.channel.send(content=None, embed=search)


@client.command(name='lang')
async def set_lang(context: commands.context.Context):
    words = context.message.content.split()
    lang = ' '.join(words[1:])
    if lang == '':
        err = discord.Embed(title='Enter language!',
                            description=f'{prefix}help - to view the list of commands and languages',
                            color=discord.Color.dark_red())
        await context.channel.send(content=None, embed=err)
    else:
        wikipedia.set_lang(prefix=lang)
        msg = discord.Embed(title='Language changed!', description=f'Currently language: "{lang}"',
                            color=discord.Color.orange())
        await context.channel.send(content=None, embed=msg)


@client.command(name='help')
async def help(context: commands.context.Context):
    msg = discord.Embed(title='Command list:',
                        description=f'{prefix}help - call the command list\n\n'
                                    f'{prefix}s - search by request\n\n'
                                    f'{prefix}lang - change search language:\nru - russian'
                                    '\nen - english\nfr - french'
                                    '\nde - german\nit - italian'
                                    '\nes - spanish\nzh - chinese'
                                    '\nja - japanese\nar - arabian'
                                    '\nuk - ukrainian\n',
                        color=discord.Color.orange())
    await context.channel.send(content=None, embed=msg)


client.run(config.token)