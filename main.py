import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)

for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run("Nzc2NjI5MzY5NDQ3MjUyMDE4.X63qdg.GI7N6pQV_yFFpiJXCUO4VhA0BK4")

