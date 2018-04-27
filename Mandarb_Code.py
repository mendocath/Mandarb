import discord
from discord.ext import commands
import asyncio
import logging
import random
import datetime
import configparser
from time import gmtime, strftime

config = configparser.RawConfigParser()
configFilePath = r'bot_config.conf'

try:
    config.read(configFilePath)
except:
    print("Error loading config!  Please check config file 'bot-config.conf'")

DISCORD_AUTH_TOKEN = config.get('bot-config', 'discord_auth_token')

def tchatLogger(server, channel, author, messagetype, message = ""):
    with open(server + "_" + channel + strftime('_%Y%m%d')+ ".log", 'a') as the_file:
        the_file.write(strftime('%Y-%m-%d_%H:%M:%S') + "§" + author + "§" + messagetype + "§" + message+"\n")

description = ''' Test bot for Mendo'''

bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    cattachments = ""
    if len(message.attachments) != 0:
        cattachments = ''.join(str(e) for e in message.attachments)
    tchatLogger(str(message.server),str(message.channel),message.author.name,"Text",message.content + (("§" + cattachments) if cattachments != "" else "" ))
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message):
    cattachments = ""
    if len(message.attachments) != 0:
        cattachments = ''.join(str(e) for e in message.attachments)
    tchatLogger(str(message.server),str(message.channel),message.author.name,"Deleted",message.content +  (("§" + cattachments) if cattachments != "" else "" ))
@bot.event
async def on_message_edit(before, after):
    tchatLogger(str(before.server),str(before.channel),before.author.name,"Edit",before.content + " -> " + after.author.name +    "§" + after.content)
@bot.event
async def on_reaction_add(reaction, user):
    tchatLogger(str(reaction.message.server),str(reaction.message.channel),reaction.message.author.name,"Reaction_add",str(reaction.emoji) + "§" + reaction.message.content )
@bot.event
async def on_reaction_remove(reaction, user):
    tchatLogger(str(reaction.message.server),str(reaction.message.channel),reaction.message.author.name,"Reaction_remove",str(reaction.emoji) + "§" + reaction.message.content )


@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

bot.run(DISCORD_AUTH_TOKEN)


    