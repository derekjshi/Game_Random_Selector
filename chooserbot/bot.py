# bot.py
import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from chooserbot.db import Database, getDatabase
from chooserbot.tables import UsersTable, ItemsTable, ResultsTable
from chooserbot.randomizer import GameRandomizer, RandomizerInterface

'''
db = None
users_tables = UsersTable("Users")
items_table = ItemsTable("Items")
results_table = ResultsTable("Results")
'''

class DiscordBot(discord.Client):

    def __init__(self, randomizer: RandomizerInterface, db: Database, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.randomizer = randomizer
        self.db = db
            
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
        elif '!chooser game add' in message.content.lower():
            #todo need to parse message better and add game that's mentioned
            #response = 'TODO - NOT IMPLEMENTED'

            #crude implementation
            words = message.content.split()
            item = ' '.join(words[3:])

            user = self.db.users_table.get_user(self.db.db, message.author.name) 

            if len(user) == 0:
                self.db.users_table.create_entity(self.db.db, message.author.name)
                user = self.db.users_table.get_user(self.db.db, message.author.name)

            self.db.items_table.create_entity(self.db.db, item, user[0][0])
            response = user[0][1] + " added " + item

        elif message.content.lower() == '!chooser game list':
            response = 'TODO - NOT IMPLEMENTED'
        elif message.content.lower() == '!chooser game remove':
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
    db = getDatabase() 
    items = db.items_table.retrieve_all(db.db)

    item_list = []

    for item in items:
        print(item)
        item_list.append(item[1])


    r1 = GameRandomizer(item_list)
    #r1 = GameRandomizer(["Valorant", "Minecraft", "Runescape", "League of Legends", "L4D2"])
    discord_client = DiscordBot(r1, db)
    discord_client.run(TOKEN)
