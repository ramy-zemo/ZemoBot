import os
import discord
import logging
import json

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

for language_file in os.listdir("languages"):
    with open("languages/" + language_file, "r", encoding="UTF-8") as file:
        language_content = json.loads(file.read())

    language_name = language_file[:language_file.index(".")]
    exec(f"bot.{language_name} = language_content")


for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")


def language(discord_bot, lang, keyword, **kwargs):
    all_keywords = getattr(discord_bot, lang)

    for val in kwargs:
        locals()[val] = kwargs[val]

    return eval(f'f"""{all_keywords[keyword]}"""')


def get_guild_language(self, guild_id):
    lang = self.bot.ApiClient.request(self.bot.ApiClient.get_language, params={"guild_id": str(guild_id)})
    return lang if lang else "en"


guild_languages = {}

bot.guild_languages = guild_languages
bot.get_guild_language = get_guild_language
bot.language = language

bot.run(DISCORD_TOKEN)
