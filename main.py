import os
import discord
from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None, description="Nice Allrounder Bot, coded by Ramo")

for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

token = os.getenv('DISCORD_TOKEN')
bot.run(token)
