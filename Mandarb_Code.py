import discord
 from discord.ext import commands
 import asyncio
 import logging
 import random
 import datetime
 import configparser

 config = configparser.RawConfigParser()
 configFilePath = r'bot_config.conf'

 try:
     config.read(configFilePath)
 except:
     print("Error loading config!  Please check config file 'bot-config.conf'")

 DISCORD_AUTH_TOKEN = config.get('bot-config', 'discord_auth_token')

 logger = logging.getLogger('discord')
 logger.setLevel(logging.INFO)
 handler = logging.FileHandler(filename='discord.log', encoding='utf-8')
 handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
 logger.addHandler(handler)

 generallogger = logging.getLogger('discord.general')
 generallogger.setLevel(logging.INFO)
 handler = logging.FileHandler(filename='discord.general.log', encoding='utf-8')
 handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
 generallogger.addHandler(handler)

 channel2logger = logging.getLogger('discord.channel2')
 channel2logger.setLevel(logging.INFO)
 handler = logging.FileHandler(filename='discord.channel2.log', encoding='utf-8')
 handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
 channel2logger.addHandler(handler)


 description = ''' Mandarb bot for TV Discord '''

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
     if message.channel.name == "general":
         generallogger.info(message.author.name + " : " + message.content + " : " + cattachments)
     if message.channel.name == "channel2":
         channel2logger.info(message.author.name + " : " + message.content + " : " + cattachments)

     await bot.process_commands(message)

 @bot.event
 async def on_message_delete(message):
     cattachments = ""
     if len(message.attachments) != 0:
         cattachments = ''.join(str(e) for e in message.attachments)
     if message.channel.name == "general":
         generallogger.info("Deleted : " + message.author.name + " : " + message.content + " : " + cattachments)
     if message.channel.name == "channel2":
        cattachments = ''.join(str(e) for e in message.attachments)
         channel2logger.info("Deleted : " + message.author.name + " : " + message.content + " : " + cattachments)

 @bot.event
 async def on_message_edit(before, after):
     if before.channel.name == "general":
         generallogger.info("Edit: " + before.author.name + " : " + before.content + " -> " + after.author.name +     " :  " +  after.content)
     if before.channel.name == "channel2":
         channel2logger.info("Edit: " + before.author.name + " : " +  before.content + " -> " + after.author.         name +    " : " + after.content)

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
