import discord
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

conn_main = mysql.connector.connect(
    host=os.getenv('db_ip'),
    user=os.getenv('db_user'),
    password=os.getenv('db_password'),
    database=os.getenv('db_database')
)
cur_main = conn_main.cursor()


def get_all_twitch_data():
    cur_main.execute('SELECT SERVER, TWITCH_USERNAME FROM CONFIG')
    return cur_main.fetchall()


def get_twitch_username(ctx):
    cur_main.execute('SELECT TWITCH_USERNAME FROM CONFIG WHERE SERVER = %s', ([ctx.guild.id]))
    cur_main.fetchall()


def update_twitch_username(ctx, username):
    cur_main.execute('UPDATE CONFIG SET TWITCH_USERNAME = %s WHERE SERVER = %s', (username, str(ctx.guild.id)))
    conn_main.commit()


def insert_user_xp(ctx, user, xp):
    sql = "INSERT INTO LEVEL (server, user, xp) VALUES (%s, %s, %s)"
    val_1 = (str(ctx.guild.id), str(user), int(xp))

    cur_main.execute(sql, val_1)
    conn_main.commit()


def update_user_xp(ctx, user, new_xp):
    sql = "UPDATE LEVEL SET xp=%s WHERE server=%s AND user=%s"
    val_1 = (new_xp, str(ctx.guild.id), str(user))

    cur_main.execute(sql, val_1)
    conn_main.commit()


def get_xp_from_user(ctx, user):
    cur_main.execute("SELECT * FROM LEVEL WHERE server=%s AND user=%s", (str(ctx.guild.id), str(user)))
    return cur_main.fetchall()


def get_server_ranks(ctx):
    cur_main.execute("SELECT * FROM LEVEL WHERE server=%s ORDER BY xp ASC", ([str(ctx.guild.id)]))
    return cur_main.fetchall()


def setup_db(ctx, amout):
    for user in ctx.guild.users:
        cur_main.execute("INSERT INTO LEVEL (server, user, xp) VALUES (%s, %s, %s)", ([ctx.guild.id, str(user), amout]))
        conn_main.commit()


async def get_main_channel(ctx):
    try:
        guild = ctx.guild
    except AttributeError:
        guild = ctx

    cur_main.execute("SELECT MESSAGE_CHANNEL FROM CONFIG WHERE server=%s", ([ctx.id]))
    channel = cur_main.fetchall()

    overwrites_main = {
        guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True,
                                                        send_messages=False)
    }

    if channel:
        if not discord.utils.get(guild.channels, id=int(channel[0][0])):
            main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)
            change_msg_welcome_channel(guild, main_channel, main_channel)
            return main_channel
    else:
        main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)
        change_msg_welcome_channel(guild, main_channel, main_channel)
        return main_channel


async def get_welcome_channel(ctx):
    try:
        guild = ctx.guild
    except:
        guild = ctx

    try:
        cur_main.execute("SELECT WELCOME_CHANNEL FROM CONFIG WHERE server=%s", ([guild.id]))
        k = cur_main.fetchall()
        channel_id = k[0][0]
        channel = discord.utils.get(guild.channels, id=int(channel_id))

    except:
        channel = discord.utils.get(guild.channels, name="willkommen")

    return channel


def get_user_messages(user):
    cur_main.execute("SELECT * from MESSAGE WHERE von=%s", (user,))
    return cur_main.fetchall()


def get_user_voice_time(user):
    cur_main.execute("SELECT minutes from VOICE WHERE user=%s", (str(user),))
    data = cur_main.fetchall()
    return data[0][0] if data else 0


def add_user_voice_time(user, minutes):
    cur_main.execute("UPDATE VOICE SET minutes = minutes + %s WHERE user=%s", ([minutes, str(user)]))
    conn_main.commit()


def insert_user_voice_time(user, minutes):
    cur_main.execute("INSERT INTO VOICE (user, minutes) VALUES (%s , %s)", ([str(user), minutes]))
    conn_main.commit()


def get_user_trashtalk(guild_id, user):
    cur_main.execute(f"SELECT * FROM TrashTalk WHERE server=%s AND von=%s", [str(guild_id), str(user)])
    return cur_main.fetchall()


def reset_trashtalk(guild_id, user):
    try:
        cur_main.execute(f"DELETE FROM TrashTalk WHERE server=%s AND von=%s", (str(guild_id), str(user)))
        conn_main.commit()
        return 1

    except:
        return 0


def get_invites_to_user(server, invite_to):
    cur_main.execute("SELECT * FROM INVITES WHERE server = %s AND an=%s", ([str(server), str(invite_to)]))
    return cur_main.fetchall()


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
    cur_main.execute('CREATE TABLE IF NOT EXISTS INVITES ( server TEXT, datum TEXT, von TEXT, an TEXT)')
    cur_main.execute('CREATE TABLE IF NOT EXISTS LEVEL ( server TEXT, user TEXT, xp INT)')
    cur_main.execute('CREATE TABLE IF NOT EXISTS MESSAGE ( server TEXT, datum TEXT, von TEXT, nachricht TEXT)')
    cur_main.execute('CREATE TABLE IF NOT EXISTS TRASHTALK ( server TEXT, datum TEXT, von TEXT, an TEXT)')
    cur_main.execute('CREATE TABLE IF NOT EXISTS VOICE ( user TEXT, minutes INT)')
    cur_main.execute('CREATE TABLE IF NOT EXISTS PARTNER ( server TEXT, user TEXT)')
    cur_main.execute('CREATE TABLE IF NOT EXISTS CONFIG ( ACTIVE TEXT, SERVER TEXT, SPRACHE TEXT, PREFIX TEXT,'
                     ' MESSAGE_CHANNEL TEXT, WELCOME_TEXT TEXT, WELCOME_ROLE TEXT,'
                     ' WELCOME_CHANNEL TEXT, DISABLED_COMMANDS TEXT, TWITCH_USERNAME TEXT)')
    conn_main.commit()


def log_message(server, date, message):
    sql = "INSERT INTO MESSAGE (server, datum, von, nachricht) VALUES (%s, %s, %s, %s)"
    val_1 = (str(server), str(date), str(message.author), str(message.content))

    cur_main.execute(sql, val_1)
    conn_main.commit()

    return 1


def log_invite(server, datum, von, an):
    sql = "INSERT INTO MESSAGE (server, datum, von, nachricht) VALUES (%s, %s, %s, %s)"
    val_1 = (server, datum, von, an)

    cur_main.execute(sql, val_1)
    conn_main.commit()

    return 1


def log_trashtalk(ctx, datum, user):
    sql = "INSERT INTO TrashTalk (server, datum, von, an) VALUES (%s, %s, %s, %s)"
    val_1 = (str(ctx.guild.id), datum, str(ctx.message.author), str(user))

    cur_main.execute(sql, val_1)
    conn_main.commit()


def change_msg_welcome_channel(guild, main_channel, welcome_channel):
    sql = "UPDATE CONFIG SET MESSAGE_CHANNEL=%s, WELCOME_CHANNEL = %s WHERE server=%s"
    val_1 = (str(main_channel.id), str(welcome_channel.id), str(guild.id))

    cur_main.execute(sql, val_1)
    conn_main.commit()

    return 1


def setup_config(guild, main_channel, welcome_channel):
    sql = "INSERT INTO CONFIG (ACTIVE, SERVER, SPRACHE, PREFIX, MESSAGE_CHANNEL, WELCOME_TEXT, WELCOME_CHANNEL) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    val = ("True", str(guild.id), "german", "$", str(main_channel.id),
           'Selam {member}, willkommen in der Familie!\nHast du Ärger, gehst du Cafe Al Zemo, gehst du zu Ramo!\n Eingeladen von: {inviter}',
           str(welcome_channel.id))

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
