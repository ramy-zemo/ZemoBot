from sql.general import conn_main, cur_main, decode_data, InvalidGuild
import discord


def activate_guild(guild_id: int):
    sql = "UPDATE CONFIG SET ACTIVE = TRUE WHERE GUILD_ID = %s"
    val = (guild_id,)

    cur_main.execute(sql, val)
    conn_main.commit()


def deactivate_guild(guild_id: int):
    sql = "UPDATE CONFIG SET ACTIVE = FALSE WHERE GUILD_ID = %s"
    val = (guild_id,)

    cur_main.execute(sql, val)
    conn_main.commit()


def change_prefix(guild_id: int, prefix: str):
    sql = "UPDATE CONFIG SET PREFIX = %s WHERE GUILD_ID = %s"
    val = (prefix, guild_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def get_prefix(guild_id: int) -> int:
    sql = "SELECT PREFIX FROM CONFIG WHERE GUILD_ID=%s"
    val = (guild_id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchone()
    return data[0] if data else 0


def setup_config(guild_id: int, main_channel_id: int, welcome_channel_id: int):
    sql = "INSERT INTO CONFIG (ACTIVE, GUILD_ID, LANGUAGE, PREFIX, MESSAGE_CHANNEL_ID, WELCOME_CHANNEL_ID) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (True, guild_id, "german", "$", main_channel_id, welcome_channel_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def change_msg_welcome_channel(guild_id: int, main_channel_id: int, welcome_channel_id: int):
    sql = "UPDATE CONFIG SET MESSAGE_CHANNEL_ID=%s, WELCOME_CHANNEL_ID=%s WHERE GUILD_ID=%s"
    val_1 = (main_channel_id, welcome_channel_id, guild_id)

    cur_main.execute(sql, val_1)
    conn_main.commit()


def delete_all_configs():
    cur_main.execute("TRUNCATE TABLE config;")
    conn_main.commit()


def get_server(guild_id: int) -> bool:
    cur_main.execute('SELECT ACTIVE FROM CONFIG WHERE GUILD_ID = %s', (guild_id,))
    data = cur_main.fetchone()

    return bool(data)


def get_all_twitch_data() -> list:
    cur_main.execute('SELECT GUILD_ID, TWITCH_USERNAME FROM CONFIG')
    data = cur_main.fetchall()
    return [entry for entry in decode_data(data) if entry[1]]


def get_twitch_username(guild_id: int) -> str:
    cur_main.execute('SELECT TWITCH_USERNAME FROM CONFIG WHERE GUILD_ID = %s', (guild_id,))
    data = cur_main.fetchone()
    return data[0] if data and data[0] else ""


def update_twitch_username(guild_id: int, twitch_username: str):
    cur_main.execute('UPDATE CONFIG SET TWITCH_USERNAME = %s WHERE GUILD_ID = %s', (twitch_username, guild_id))
    conn_main.commit()


async def get_main_channel(ctx) -> discord.TextChannel:
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
            change_msg_welcome_channel(guild.id, main_channel.id, main_channel.id)
            return main_channel
        else:
            return channel
    else:
        main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)
        change_msg_welcome_channel(guild.id, main_channel.id, main_channel.id)
        return main_channel


async def get_welcome_channel(ctx) -> discord.TextChannel:
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
            change_msg_welcome_channel(guild.id, welcome_channel.id, welcome_channel.id)
            return welcome_channel
        else:
            return channel
    else:
        welcome_channel = await guild.create_text_channel(name="willkommen", overwrites=overwrites_main)
        change_msg_welcome_channel(guild.id, welcome_channel.id, welcome_channel.id)
        return welcome_channel


def change_auto_role(guild_id: int, role_id: int):
    sql = "UPDATE CONFIG SET WELCOME_ROLE_ID = %s WHERE GUILD_ID = %s"
    val = (role_id, guild_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def get_welcome_role_id(guild_id: int) -> int:
    sql = "SELECT WELCOME_ROLE_ID FROM CONFIG WHERE GUILD_ID=%s"
    val = (str(guild_id),)

    cur_main.execute(sql, val)

    data = cur_main.fetchone()

    return data[0] if data else 0


def get_welcome_role(guild: discord.guild):
    sql = "SELECT WELCOME_ROLE_ID FROM CONFIG WHERE GUILD_ID=%s"
    val = (guild.id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchone()

    role = ""

    if data and data[0]:
        role = discord.utils.get(guild.roles, id=int(data[0]))

    return role if role else 0


def get_welcome_message(guild_id: int) -> str:
    sql = "SELECT WELCOME_MESSAGE FROM CONFIG WHERE GUILD_ID=%s"
    val = (guild_id,)

    cur_main.execute(sql, val)

    data = cur_main.fetchone()

    return data[0] if data and data[0] and data[0] else ""


def change_welcome_message(guild_id: int, welcome_msg: str):
    sql = "UPDATE CONFIG SET WELCOME_MESSAGE=%s WHERE GUILD_ID=%s"
    val = (welcome_msg, guild_id)

    cur_main.execute(sql, val)

    conn_main.commit()