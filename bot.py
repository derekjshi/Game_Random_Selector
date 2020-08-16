# bot.py
import os
import random

from GameRandomizer import RandomizerInterface

import discord
from discord.ext import commands

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