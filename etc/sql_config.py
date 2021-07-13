import discord
import mysql.connector

from config import DB_IP, DB_USER, DB_PASSWORD, DB_DATABASE


class InvalidGuild(Exception):
    pass


async def get_main_channel(API_CLIENT, ctx) -> discord.TextChannel:
    conn_main = mysql.connector.connect(
        host=DB_IP,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cur_main = conn_main.cursor()

    try:
        guild = ctx.guild
    except AttributeError:
        guild = ctx

    cur_main.execute("SELECT MESSAGE_CHANNEL_ID FROM CONFIG WHERE GUILD_ID=%s", (guild.id,))
    channel_db = cur_main.fetchone()

    overwrites_main = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True,
                                                        send_messages=False)
    }

    if channel_db:
        channel = discord.utils.get(guild.channels, id=int(channel_db[0]))
        if not channel:
            main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)
            API_CLIENT.request(API_CLIENT.change_msg_welcome_channel,
                               params={"guild_id": guild.id,
                                       "main_channel_id": main_channel.id,
                                       "welcome_channel_id": main_channel.id})

            return main_channel
        else:
            return channel
    else:
        main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)
        API_CLIENT.request(API_CLIENT.change_msg_welcome_channel,
                           params={"guild_id": guild.id,
                                   "main_channel_id": main_channel.id,
                                   "welcome_channel_id": main_channel.id})

        return main_channel


async def get_welcome_channel(API_CLIENT, ctx) -> discord.TextChannel:
    conn_main = mysql.connector.connect(
        host=DB_IP,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cur_main = conn_main.cursor()

    try:
        guild = ctx.guild
    except AttributeError:
        guild = ctx

    cur_main.execute("SELECT WELCOME_CHANNEL_ID FROM CONFIG WHERE GUILD_ID=%s", (guild.id,))
    channel_db = cur_main.fetchall()

    overwrites_main = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True,
                                                        send_messages=False)
    }

    if channel_db:
        channel = discord.utils.get(guild.channels, id=int(channel_db[0][0]))
        if not channel:
            welcome_channel = await guild.create_text_channel(name="willkommen", overwrites=overwrites_main)

            # todo: Das ist pfusch da es keinen API endpoint gibt der nur den welcome channel ändern.
            #  Muss erstellt werden.

            main_channel = await get_main_channel(API_CLIENT, ctx)

            API_CLIENT.request(API_CLIENT.change_msg_welcome_channel,
                               params={"guild_id": guild.id,
                                       "main_channel_id": main_channel.id,
                                       "welcome_channel_id": welcome_channel.id})

            return welcome_channel
        else:
            return channel
    else:
        welcome_channel = await guild.create_text_channel(name="willkommen", overwrites=overwrites_main)
        main_channel = await get_main_channel(API_CLIENT, ctx)

        API_CLIENT.request(API_CLIENT.change_msg_welcome_channel,
                           params={"guild_id": guild.id,
                                   "main_channel_id": main_channel.id,
                                   "welcome_channel_id": welcome_channel.id})
        return welcome_channel


def get_welcome_role(guild: discord.guild):
    conn_main = mysql.connector.connect(
        host=DB_IP,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )
    cur_main = conn_main.cursor()

    sql = "SELECT WELCOME_ROLE_ID FROM CONFIG WHERE GUILD_ID=%s"
    val = (guild.id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchone()

    role = ""

    if data and data[0]:
        role = discord.utils.get(guild.roles, id=int(data[0]))

    return role if role else 0
