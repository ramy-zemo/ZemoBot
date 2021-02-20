import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Solid Base made by Nikola
# https://github.com/Anunakif0x

load_dotenv()

logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="prefix_not_set_wvAfKULVKgApPPO", intents=intents,
                   help_command=None, description="Nice multipurpose Bot, coded by Ramo")

bot.user_commands = ["trashtalk", "trashtalk_stats", "trashtalk_reset", "trashtalk_list", "trashtalk_add", "mafia",
                     "ping", "stats", "auszeit", "meme", "font", "font_list", "invite", "w2g", "info", "trump",
                     "trump_img", "gen_meme", "twitch_setup", "show_roles", "show_channels", "set_xp", "avatar", "help",
                     "invite_bot", "ban", "kick", "unban", "faceit_finder", "set_auto_role", "google", "set_prefix",
                     "enable_command", "disable_command", "invites", "server_info", "partner", "coin", "pick_number",
                     "setup_db", "rank", "add_xp", "get_rank", "setup", "setup_twitch"]

for filename in os.listdir("cogs"):
    if filename.endswith(".py") and filename != "__init__.py":
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv('DISCORD_TOKEN'))
