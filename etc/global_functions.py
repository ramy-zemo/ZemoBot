import discord
import sqlite3
import asyncio

conn_main = sqlite3.connect("main.db")
cur_main = conn_main.cursor()


async def get_main_channel(ctx):
    try:
        guild = ctx.guild
    except:
        guild = ctx
    try:
        cur_main.execute("SELECT main_channel FROM CONFIG WHERE server=?", ([guild.id]))
        k = cur_main.fetchall()
        channel_id = k[0][1]
        channel = discord.utils.get(guild.channels, id=int(channel_id))

    except IndexError:
        channel = discord.utils.get(guild.channels, name="zemo-bot")

    return channel


