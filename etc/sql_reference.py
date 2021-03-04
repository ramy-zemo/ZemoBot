import discord
import mysql.connector

from dotenv import load_dotenv
from config import DB_IP, DB_USER, DB_PASSWORD, DB_DATABASE


load_dotenv()

conn_main = mysql.connector.connect(
    host=DB_IP,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)
cur_main = conn_main.cursor()


class InvalidGuild(Exception):
    pass


def decode_data(data) -> list:
    new_data = list()
    for data_set in data:
        entry = list()
        for item in data_set:
            if isinstance(item, bytes):
                entry.append(item.decode())
            else:
                entry.append(item)
        new_data.append(entry)
    return new_data


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
    return data[0] if data else ""


def update_twitch_username(guild_id: int, twitch_username: str):
    cur_main.execute('UPDATE CONFIG SET TWITCH_USERNAME = %s WHERE GUILD_ID = %s', (twitch_username, guild_id))
    conn_main.commit()


def insert_user_xp(guild_id: int, user_id: int, xp: int):
    sql = "INSERT INTO LEVEL (SERVER_ID, USER_ID, XP) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s)"
    val_1 = (guild_id, user_id, xp)

    try:
        cur_main.execute(sql, val_1)
        conn_main.commit()
    except mysql.connector.errors.IntegrityError:
        raise InvalidGuild


def get_xp_from_user(guild_id: int, user_id: int) -> int:
    cur_main.execute("SELECT SUM(XP) FROM LEVEL WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND USER_ID=%s", (guild_id, user_id))
    data = cur_main.fetchone()

    return data[0] if data else 0


def get_server_ranks(guild_id: int) -> list:
    sql = "SELECT * FROM LEVEL WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) ORDER BY XP ASC"
    val = (guild_id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()

    new = {}
    done_users = []

    for entry in decode_data(data):
        if entry[1] in done_users:
            continue

        for second in decode_data(data):
            if second[0] == entry[0] and second[1] == entry[1]:
                if second[1] in new:
                    new[second[1]] += second[2]
                else:
                    new[second[1]] = second[2]

        done_users.append(entry[1])

    return [(k, v) for k, v in new.items()]


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


def get_user_messages(user_id: int) -> list:
    cur_main.execute("SELECT * from MESSAGE WHERE USER_ID=%s", (user_id,))
    data = cur_main.fetchall()
    return decode_data(data)


def get_user_voice_time(user_id: int) -> int:
    cur_main.execute("SELECT SUM(MINUTES) from VOICE WHERE USER_ID=%s", (user_id,))
    data = cur_main.fetchone()
    return data[0] if data else 0


def add_user_voice_time(user_id: int, minutes: int, guild_id: int):
    sql = "INSERT INTO VOICE (SERVER_ID, USER_ID, MINUTES) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s)"
    val = (guild_id, user_id, minutes)

    cur_main.execute(sql, val)
    conn_main.commit()


def get_user_trashtalk(guild_id: int, user_id: int) -> list:
    sql = "SELECT * FROM TRASHTALK_LOG WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND FROM_USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()
    return decode_data(data)


def reset_trashtalk(guild_id: int, user_id: int):
    sql = "DELETE FROM TRASHTALK_LOG WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND FROM_USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def get_invites_to_user(guild_id: int, invite_to_user_id: int) -> list:
    sql = "SELECT * FROM INVITES WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND TO_USER_ID=%s"
    val = (guild_id, invite_to_user_id)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()
    return decode_data(data)


async def get_user_invites(guild_id: int, user_id: int) -> list:
    sql = "SELECT * FROM INVITES WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND FROM_USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)
    invites = cur_main.fetchall()
    return invites


def log_message(guild_id: int, date: str, user_id: int, message: str):
    sql = "INSERT INTO MESSAGE (SERVER_ID, DATE, USER_ID, MESSAGE) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, date, user_id, message)

    cur_main.execute(sql, val)
    conn_main.commit()


def log_invite(guild_id: int, date: str, from_user_id: int, to_user_id: int):
    sql = "INSERT INTO INVITES (SERVER_ID, DATE, FROM_USER_ID, TO_USER_ID) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, date, from_user_id, to_user_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def log_trashtalk(guild_id: int, datum: str, from_user_id: int, to_user_id: int):
    sql = "INSERT INTO TRASHTALK_LOG (SERVER_ID, DATE, FROM_USER_ID, TO_USER_ID) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, datum, from_user_id, to_user_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def change_msg_welcome_channel(guild_id: int, main_channel_id: int, welcome_channel_id: int):
    sql = "UPDATE CONFIG SET MESSAGE_CHANNEL_ID=%s, WELCOME_CHANNEL_ID=%s WHERE GUILD_ID=%s"
    val_1 = (main_channel_id, welcome_channel_id, guild_id)

    cur_main.execute(sql, val_1)
    conn_main.commit()


def setup_config(guild_id: int, main_channel_id: int, welcome_channel_id: int):
    sql = "INSERT INTO CONFIG (ACTIVE, GUILD_ID, LANGUAGE, PREFIX, MESSAGE_CHANNEL_ID, WELCOME_CHANNEL_ID) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (True, guild_id, "german", "$", main_channel_id, welcome_channel_id)

    cur_main.execute(sql, val)
    conn_main.commit()


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


def delete_all_configs():
    cur_main.execute("TRUNCATE TABLE config;")
    conn_main.commit()


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

    return data[0]if data else 0


def get_prefix(guild_id: int) -> int:
    sql = "SELECT PREFIX FROM CONFIG WHERE GUILD_ID=%s"
    val = (guild_id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchone()
    return data[0]if data else 0


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

    return data[0] if data and data[0] else ""


def check_command_status_for_guild(guild_id: int, command: str):
    sql = "SELECT * FROM DISABLED_COMMANDS WHERE COMMAND_ID=(SELECT ID FROM COMMANDS WHERE COMMAND=%s) AND SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)"
    val = (command, guild_id)

    cur_main.execute(sql, val)
    data = cur_main.fetchone()
    return not data


def disable_command(guild_id: int, command: str):
    cur_main.execute("SELECT ID FROM COMMANDS WHERE COMMAND=%s", (command,))
    command_in_db = cur_main.fetchone()

    if command_in_db:
        sql = "INSERT INTO DISABLED_COMMANDS (SERVER_ID, COMMAND_ID) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s)"
        val = (guild_id, command_in_db[0])

        cur_main.execute(sql, val)
        conn_main.commit()


def enable_command(guild_id: int, command: str):
    if check_command_status_for_guild(guild_id, command):
        return

    sql = "DELETE FROM DISABLED_COMMANDS WHERE COMMAND_ID=(SELECT ID FROM COMMANDS WHERE COMMAND=%s) AND SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)"
    val = (command, guild_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def change_welcome_message(guild_id: int, welcome_msg: str):
    sql = "UPDATE CONFIG SET WELCOME_MESSAGE=%s WHERE GUILD_ID=%s"
    val = (welcome_msg, guild_id)

    cur_main.execute(sql, val)

    conn_main.commit()


def get_all_disabled_commands_from_guild(guild_id: int) -> list:
    cur_main.execute("SELECT COMMAND_ID FROM DISABLED_COMMANDS WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)", (guild_id,))
    command_ids = cur_main.fetchall()
    data = []

    for command_id in command_ids:
        cur_main.execute("SELECT COMMAND FROM COMMANDS WHERE ID=%s", command_id)
        data.append(cur_main.fetchone()[0])

    return data


def update_user_xp(guild_id: int, user_id: int, xp: int):
    cur_main.execute("DELETE FROM LEVEL WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND USER_ID=%s", (guild_id, user_id))
    conn_main.commit()

    sql = "INSERT INTO LEVEL (SERVER_ID, USER_ID, XP) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s)"
    val = (guild_id, user_id, xp)

    cur_main.execute(sql, val)
    conn_main.commit()


def get_all_guild_commands(guild_id: int):
    cur_main.execute("SELECT CATEGORY_ID, COMMAND FROM COMMANDS WHERE ID NOT IN (SELECT COMMAND_ID FROM DISABLED_COMMANDS WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s))", (guild_id,))
    commands = {command: category for (category, command) in cur_main.fetchall()}

    for command in commands:
        cur_main.execute("SELECT CATEGORY FROM COMMAND_CATEGORIES WHERE ID=%s", (commands[command],))
        commands[command] = cur_main.fetchone()[0]

    return commands
