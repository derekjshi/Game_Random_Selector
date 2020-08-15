from GameRandomizer import GameSelector
from bot import DiscordBot

import discord
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')

    # TODO switch for dynamic loading from some file or etc.
    r1 = GameSelector(["Valorant", "Minecraft", "Runescape", "League of Legends", "L4D2"])
    discord_client = DiscordBot(r1)
    discord_client.run(TOKEN)

if __name__ == "__main__":
    main()
