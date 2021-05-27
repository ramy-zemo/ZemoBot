import os
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv
from config import DISCORD_TOKEN, ICON_URL, ADMIN_IDS, ZEMO_API_KEY
from ZemoLogger import ZemoLogger
from ZemoBotAPIClient.ZemoBotAPIClient import ZemoBotApiClient


# Solid Base made by Nikola
# https://github.com/Anunakif0x

load_dotenv()
logging.basicConfig(filename='zemobot.log', encoding='utf-8', level=logging.ERROR)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="prefix_not_set_wvAfKULVKgApPPO", intents=intents,
                   help_command=None, description="Nice multipurpose Bot, coded by Ramo")

ApiClient = ZemoBotApiClient(API_KEY=ZEMO_API_KEY)
bot.ApiClient = ApiClient

bot.icon_url = ICON_URL
bot.admin_ids = ADMIN_IDS
bot.logger = ZemoLogger(logging_level="DEBUG", file_name="zemobot_log.txt")

for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(DISCORD_TOKEN)
