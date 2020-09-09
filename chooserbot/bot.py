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

        self.get_item_list_from_db()

        if ';' in message.content:
            message = "No semicolons allowed you hacker."
        elif message.content.lower() == '!chooser game':
            response = self.randomizer.pick_item()
        elif '!chooser game add' in message.content.lower():
            response = self.parse_game_add_msg(message)
        elif message.content.lower() == '!chooser game list':
            item_list = self.get_item_list_from_db()
            response = "List:\n" + '\n'.join(item_list)
        elif '!chooser game remove' in message.content.lower():
            response = self.parse_game_remove_msg(message)
        else:
            response = 'TODO - Help Message'

        await message.channel.send(response)

    def get_item_list_from_db(self):
        item_tuples = self.db.items_table.retrieve_all(self.db.db)
        item_list = []

        for item in item_tuples:
            item_list.append(item[1])

        return item_list

    def update_item_list_from_db(self):
        item_list = self.get_item_list_from_db()
        self.randomizer.set_list_of_games(item_list)

    def parse_game_add_msg(self, message):
        #crude implementation
        words = message.content.split()
        item = ' '.join(words[3:])

        user_tuple = self.db.users_table.retrieve_entity(self.db.db, entity_name=message.author.name) 

        if len(user_tuple) == 0:
            self.db.users_table.create_entity(self.db.db, message.author.name)
            user_tuple = self.db.users_table.retrieve_entity(self.db.db, entity_name=message.author.name)

        self.db.items_table.create_entity(self.db.db, item, user_tuple[0][0])
        response = user_tuple[0][1] + " added " + item

        return response

    def parse_game_remove_msg(self, message):
        #crude implementation
        words = message.content.split()
        item = ' '.join(words[3:])

        # need to figure out success/fail
        self.db.items_table.delete_entity(self.db.db, entity_name=item)
        
        response = message.author.name + " removed " + item
        return response

def runBot():
    """
    Run the bot with the token from .env file or environment variable 'DISCORD_TOKEN'
    """
    print("Running bot . . .")

    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # TODO switch for dynamic loading from some file or etc.
    db = getDatabase() 
    item_tuples = db.items_table.retrieve_all(db.db)

    item_list = []

    for item in item_tuples:
        item_list.append(item[1])

    r1 = GameRandomizer(item_list)
    #r1 = GameRandomizer(["Valorant", "Minecraft", "Runescape", "League of Legends", "L4D2"])
    discord_client = DiscordBot(r1, db)
    discord_client.run(TOKEN)
