import discord
import mysql.connector
import os
from icecream import ic
from dotenv import load_dotenv

load_dotenv()

conn_main = mysql.connector.connect(
    host=os.getenv('db_ip'),
    user=os.getenv('db_user'),
    password=os.getenv('db_password'),
    database=os.getenv('db_database')
)
cur_main = conn_main.cursor()


def decode_data(data):
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


def get_server(guild_id):
    cur_main.execute('SELECT ACTIVE FROM CONFIG WHERE GUILD_ID = %s', ([str(guild_id)]))
    data = cur_main.fetchall()
    return [] if not data else data[0][0].decode()


def get_all_twitch_data():
    cur_main.execute('SELECT SERVER, TWITCH_USERNAME FROM CONFIG')
    data = cur_main.fetchall()
    return decode_data(data)


def get_twitch_username(guild_id):
    cur_main.execute('SELECT TWITCH_USERNAME FROM CONFIG WHERE SERVER = %s', ([str(guild_id)]))
    data = cur_main.fetchall()
    return [] if not data or data[0][0] is None else data[0][0].decode()


def update_twitch_username(guild_id, username):
    cur_main.execute('UPDATE CONFIG SET TWITCH_USERNAME = %s WHERE SERVER = %s', (username, str(guild_id)))
    conn_main.commit()


def insert_user_xp(guild_id, user, xp):
    sql = "INSERT INTO LEVEL (server, user, xp) VALUES (%s, %s, %s)"
    val_1 = (str(guild_id), str(user), int(xp))

    cur_main.execute(sql, val_1)
    conn_main.commit()


def update_user_xp(guild_id, user, new_xp):
    sql = "UPDATE LEVEL SET xp=%s WHERE server=%s AND user=%s"
    val_1 = (new_xp, str(guild_id), str(user))

    cur_main.execute(sql, val_1)
    conn_main.commit()


def get_xp_from_user(guild_id, user):
    cur_main.execute("SELECT * FROM LEVEL WHERE server=%s AND user=%s", (str(guild_id), str(user)))
    data = cur_main.fetchall()

    return decode_data(data)


def get_server_ranks(guild_id):
    cur_main.execute("SELECT * FROM LEVEL WHERE server=%s ORDER BY xp ASC", ([str(guild_id)]))
    data = cur_main.fetchall()

    return decode_data(data)


def setup_db(ctx, amout):
    for user in ctx.guild.users:
        cur_main.execute("INSERT INTO LEVEL (server, user, xp) VALUES (%s, %s, %s)", ([ctx.guild.id, str(user), amout]))
        conn_main.commit()


async def get_main_channel(ctx):
    try:
        guild = ctx.guild
    except AttributeError:
        guild = ctx

    cur_main.execute("SELECT MESSAGE_CHANNEL FROM CONFIG WHERE server=%s", ([guild.id]))
    channel_db = cur_main.fetchall()

    overwrites_main = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True,
                                                        send_messages=False)
    }

    if channel_db:
        channel = discord.utils.get(guild.channels, id=int(channel_db[0][0].decode()))
        if not channel:
            main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)
            change_msg_welcome_channel(guild.id, main_channel, main_channel)
            return main_channel
        else:
            return channel
    else:
        main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)
        change_msg_welcome_channel(guild.id, main_channel, main_channel)
        return main_channel


async def get_welcome_channel(ctx):
    try:
        guild = ctx.guild
    except AttributeError:
        guild = ctx

    cur_main.execute("SELECT WELCOME_CHANNEL FROM CONFIG WHERE server=%s", ([guild.id]))
    channel_db = cur_main.fetchall()

    overwrites_main = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True,
                                                        send_messages=False)
    }

    if channel_db:
        channel = discord.utils.get(guild.channels, id=int(channel_db[0][0].decode()))
        if not channel:
            welcome_channel = await guild.create_text_channel(name="willkommen", overwrites=overwrites_main)
            change_msg_welcome_channel(guild.id, welcome_channel, welcome_channel)
            return welcome_channel
        else:
            return channel
    else:
        welcome_channel = await guild.create_text_channel(name="willkommen", overwrites=overwrites_main)
        change_msg_welcome_channel(guild.id, welcome_channel, welcome_channel)
        return welcome_channel


def get_user_messages(user):
    cur_main.execute("SELECT * from MESSAGE WHERE von=%s", (str(user),))
    data = cur_main.fetchall()
    return decode_data(data)


def get_user_voice_time(user):
    cur_main.execute("SELECT minutes from VOICE WHERE user=%s", (str(user),))
    data = cur_main.fetchall()
    return data[0][0] if data and data[0][0] else 0


def add_user_voice_time(user, minutes):
    cur_main.execute("UPDATE VOICE SET minutes = minutes + %s WHERE user=%s", ([minutes, str(user)]))
    conn_main.commit()


def insert_user_voice_time(user, minutes):
    cur_main.execute("INSERT INTO VOICE (user, minutes) VALUES (%s , %s)", ([str(user), minutes]))
    conn_main.commit()


def get_user_trashtalk(guild_id, user):
    cur_main.execute(f"SELECT * FROM TrashTalk WHERE server=%s AND von=%s", [str(guild_id), str(user)])
    data = cur_main.fetchall()
    return decode_data(data)


def reset_trashtalk(guild_id, user):
    try:
        cur_main.execute(f"DELETE FROM TrashTalk WHERE server=%s AND von=%s", (str(guild_id), str(user)))
        conn_main.commit()
        return 1

    except:
        return 0


def get_invites_to_user(guild_id, invite_to):
    cur_main.execute("SELECT * FROM INVITES WHERE server = %s AND an=%s", ([str(guild_id), str(invite_to)]))
    data = cur_main.fetchall()
    return decode_data(data)


async def get_user_invites(guild_id, user, ctx=0):
    cur_main.execute("SELECT * FROM INVITES WHERE server=%s AND von=%s", ([str(guild_id), str(user)]))

    invites = len(cur_main.fetchall())
    if ctx == 0:
        return invites

    else:
        embed = discord.Embed(title="Invites",
                              description=f"Du hast bereits erfolgreich {invites} Personen eingeladen.", color=0x1acdee)
        embed.set_author(name="Zemo Bot",
                         icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)


def database_setup():
    cur_main.execute("CREATE TABLE IF NOT EXISTS `CONFIG` ( `ID` INT PRIMARY KEY AUTO_INCREMENT, `ACTIVE` boolean,"
                     " `GUILD_ID` INT, `SPRACHE` TEXT, `PREFIX` TEXT, `MESSAGE_CHANNEL_ID` INT,"
                     " `WELCOME_CHANNEL_ID` INT, `WELCOME_MESSAGE` TEXT, `WELCOME_ROLE_ID` INT,"
                     " `TWITCH_USERNAME` TEXT);")

    cur_main.execute("CREATE TABLE IF NOT EXISTS `INVITES` ( `ID` INT, `DATE` DATE, `FROM_USER_ID` INT,"
                     " `TO_USER_ID` INT, CONSTRAINT `INVITE_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));")

    cur_main.execute("CREATE TABLE IF NOT EXISTS `LEVEL` ( `ID` INT, `USER_ID` INT, `XP` INT,"
                     " CONSTRAINT `LEVEL_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));")

    cur_main.execute("CREATE TABLE IF NOT EXISTS `MESSAGE` ( `ID` INT, `DATE` DATE, `USER_ID` INT, `MESSAGE` TEXT,"
                     " CONSTRAINT `MESSAGE_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));")

    cur_main.execute("CREATE TABLE IF NOT EXISTS `TRASHTALK` ( `ID` INT, `DATE` DATE, `FROM_USER_ID` INT,"
                     " `TO_USER_ID` INT, CONSTRAINT `TRASHTALK_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));")

    cur_main.execute("CREATE TABLE IF NOT EXISTS `VOICE` ( `ID` INT, `USER_ID` INT, `minutes` INT,"
                     " CONSTRAINT `VOICE_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));")

    cur_main.execute("CREATE TABLE IF NOT EXISTS `COMMANDS` ( `ID` INT PRIMARY KEY AUTO_INCREMENT, `COMMAND` TEXT,"
                     " `PARAMETERS` TEXT, `DESCRIPTION` TEXT);")

    cur_main.execute("CREATE TABLE IF NOT EXISTS `DISABLED_COMMANDS` ( `ID` INT, `COMMAND_ID` INT,"
                     " CONSTRAINT `DISABLED_COMMANDS_COMMANDS` FOREIGN KEY (ID) REFERENCES CONFIG (ID),"
                     " CONSTRAINT `DISABLED_COMMANDS_COMMANDS` FOREIGN KEY (COMMAND_ID) REFERENCES COMMANDS (ID));")

    conn_main.commit()


def log_message(server, date, message):
    sql = "INSERT INTO MESSAGE (server, datum, von, nachricht) VALUES (%s, %s, %s, %s)"
    val_1 = (str(server), str(date), str(message.author), str(message.content))

    cur_main.execute(sql, val_1)
    conn_main.commit()

    return 1


def log_invite(server, datum, von, an):
    sql = "INSERT INTO INVITES (server, datum, von, an) VALUES (%s, %s, %s, %s)"
    val_1 = (server, datum, von, an)

    cur_main.execute(sql, val_1)
    conn_main.commit()

    return 1


def log_trashtalk(guild_id, datum, von, an):
    sql = "INSERT INTO TrashTalk (server, datum, von, an) VALUES (%s, %s, %s, %s)"
    val_1 = (str(guild_id), datum, str(von), str(an))

    cur_main.execute(sql, val_1)
    conn_main.commit()


def change_msg_welcome_channel(guild_id, main_channel, welcome_channel):
    sql = "UPDATE CONFIG SET MESSAGE_CHANNEL=%s, WELCOME_CHANNEL = %s WHERE server=%s"
    val_1 = (str(main_channel.id), str(welcome_channel.id), str(guild_id))

    cur_main.execute(sql, val_1)
    conn_main.commit()

    return 1


def setup_config(guild_id, main_channel, welcome_channel):
    sql = "INSERT INTO CONFIG (ACTIVE, SERVER, SPRACHE, PREFIX, MESSAGE_CHANNEL, WELCOME_TEXT, WELCOME_CHANNEL, DISABLED_COMMANDS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = ("True", str(guild_id), "german", "$", str(main_channel.id), "", str(welcome_channel.id), "")

    cur_main.execute(sql, val)
    conn_main.commit()

    return 1


def activate_guild(guild_id):
    sql = "UPDATE CONFIG SET ACTIVE = %s WHERE SERVER = %s"
    val = ("True", str(guild_id))

    cur_main.execute(sql, val)
    conn_main.commit()


def deactivate_guild(guild_id):
    sql = "UPDATE CONFIG SET ACTIVE = %s WHERE SERVER = %s"
    val = ("False", str(guild_id))

    cur_main.execute(sql, val)
    conn_main.commit()


def change_prefix(guild_id, prefix):
    sql = "UPDATE CONFIG SET PREFIX = %s WHERE SERVER = %s"
    val = (prefix, str(guild_id))

    cur_main.execute(sql, val)
    conn_main.commit()


def clear_categories():
    cur_main.execute("""TRUNCATE TABLE config;""")
    conn_main.commit()


def change_auto_role(guild_id, role_id):
    sql = "UPDATE CONFIG SET WELCOME_ROLE = %s WHERE SERVER = %s"
    val = (str(role_id), str(guild_id))

    cur_main.execute(sql, val)
    conn_main.commit()


def get_welcome_role_id(guild_id):
    sql = "SELECT WELCOME_ROLE FROM CONFIG WHERE SERVER = %s"
    val = (str(guild_id),)

    cur_main.execute(sql, val)

    data = cur_main.fetchall()

    return data[0][0].decode() if data and data[0][0] else []


def get_prefix(guild_id):
    sql = "SELECT PREFIX FROM CONFIG WHERE SERVER = %s"
    val = (str(guild_id),)

    cur_main.execute(sql, val)

    data = cur_main.fetchall()

    return data[0][0].decode() if data and data[0][0] else "$"


def get_welcome_role(guild):
    sql = "SELECT WELCOME_ROLE FROM CONFIG WHERE SERVER = %s"
    val = (str(guild.id),)

    cur_main.execute(sql, val)

    data = cur_main.fetchall()

    role = ""

    if data and data[0][0]:
        role = discord.utils.get(guild.roles, id=int(data[0][0].decode()))

    return role if role else 0


def get_welcome_message(guild_id):
    sql = "SELECT WELCOME_TEXT FROM CONFIG WHERE SERVER = %s"
    val = (str(guild_id),)

    cur_main.execute(sql, val)

    data = cur_main.fetchall()

    return data[0][0].decode() if data and data[0][0] else ""


def set_welcome_message(guild_id, welcome_msg):
    sql = "UPDATE CONFIG SET WELCOME_TEXT = %s WHERE SERVER = %s"
    val = (str(welcome_msg), str(guild_id))

    cur_main.execute(sql, val)

    conn_main.commit()


def get_disabled_commands(guild_id):
    sql = "SELECT DISABLED_COMMANDS FROM CONFIG WHERE SERVER = %s"
    val = (str(guild_id),)

    cur_main.execute(sql, val)

    data = cur_main.fetchall()

    return [x for x in data[0][0].decode().split(";") if x != ""] if data and data[0][0] else []


def disable_command(guild_id, command):
    disabled_commands = get_disabled_commands(guild_id)

    if command not in disabled_commands:
        disabled_commands.append(str(command).lower())

    sql = "UPDATE CONFIG SET DISABLED_COMMANDS = %s WHERE SERVER = %s"

    val_1 = (";".join(disabled_commands), guild_id,)

    cur_main.execute(sql, val_1)
    conn_main.commit()


def enable_command(guild_id, command):
    disabled_commands = get_disabled_commands(guild_id)

    if isinstance(command, str):
        if command.lower() in disabled_commands:
            disabled_commands.remove(command.lower())

    elif isinstance(command, list):
        for cmd in command:
            if cmd in disabled_commands:
                disabled_commands.remove(command.lower())

    sql = "UPDATE CONFIG SET DISABLED_COMMANDS = %s WHERE SERVER = %s"
    val_1 = (";".join(disabled_commands), guild_id,)

    cur_main.execute(sql, val_1)
    conn_main.commit()
