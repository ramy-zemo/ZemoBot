import discord
import sqlite3

conn_main = sqlite3.connect("main.db")
cur_main = conn_main.cursor()


async def get_main_channel(ctx):
    try:
        guild = ctx.guild
    except:
        guild = ctx

    try:
        cur_main.execute("SELECT MESSAGE_CHANNEL FROM CONFIG WHERE server=?", ([guild.id]))
        k = cur_main.fetchall()
        channel_id = k[0][0]
        channel = discord.utils.get(guild.channels, id=int(channel_id))

    except:
        channel = discord.utils.get(guild.channels, name="zemo-bot")

    return channel


async def get_welcome_channel(ctx):
    try:
        guild = ctx.guild
    except:
        guild = ctx

    try:
        cur_main.execute("SELECT WELCOME_CHANNEL FROM CONFIG WHERE server=?", ([guild.id]))
        k = cur_main.fetchall()
        channel_id = k[0][0]
        channel = discord.utils.get(guild.channels, id=int(channel_id))

    except:
        channel = discord.utils.get(guild.channels, name="willkommen")

    return channel
