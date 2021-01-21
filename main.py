import os
import discord
import logging
from dotenv import load_dotenv
from discord.ext import commands


# Solid Base made by Nikola
# https://github.com/Anunakif0x

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None,
                   description="Nice multipurpose Bot, coded by Ramo")

for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv('DISCORD_TOKEN'))
