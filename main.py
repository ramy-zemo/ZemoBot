import os
import discord

from discord.ext import commands
from dotenv import load_dotenv
from config import DISCORD_TOKEN, ICON_URL, ADMIN_IDS

# Solid Base made by Nikola
# https://github.com/Anunakif0x

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="prefix_not_set_wvAfKULVKgApPPO", intents=intents,
                   help_command=None, description="Nice multipurpose Bot, coded by Ramo")

bot.icon_url = ICON_URL
bot.admin_ids = ADMIN_IDS

for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(DISCORD_TOKEN)
