# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from chooserbot.randomizer import GameRandomizer, RandomizerInterface

class DiscordBot(discord.Client):

    def __init__(self, randomizer: RandomizerInterface, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.randomizer = randomizer
            
    async def on_ready(self):
        print('Chooser logged on as', self.user)
    
    # TODO: make better handler & delegator
    async def on_message(self, message):
        if message.author == self.user:
            return

        if "!chooser" not in message.content.lower():
            return

        response = ''
        if message.content.lower() == '!chooser game':
            response = self.randomizer.pick_item()
        elif message.content.lower() == '!chooser game add':
            #todo need to parse message better and add game that's mentioned
            response = 'TODO - NOT IMPLEMENTED'
        elif message.content.lower() == '!chooser game list':
            response = 'TODO - NOT IMPLEMENTED'
        else:
            response = 'TODO - Help Message'

        await message.channel.send(response)

def runBot():
    """
    Run the bot with the token from .env file or environment variable 'DISCORD_TOKEN'
    """
    print("Running bot . . .")

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # TODO switch for dynamic loading from some file or etc.
    r1 = GameRandomizer(["Valorant", "Minecraft", "Runescape", "League of Legends", "L4D2"])
    discord_client = DiscordBot(r1)
    discord_client.run(TOKEN)
