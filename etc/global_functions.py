import discord
import sqlite3
import asyncio

conn_main = sqlite3.connect("main.db")
cur_main = conn_main.cursor()


async def get_main_channel(ctx):
    try:
        cur_main.execute("SELECT MESSAGE_CHANNEL FROM CONFIG WHERE server=?", ([ctx.id]))
        k = cur_main.fetchall()
        channel_id = k[0][0]
        channel = discord.utils.get(ctx.channels, id=int(channel_id))

    except:
        channel = discord.utils.get(ctx.channels, name="zemo-bot")

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


def get_user_messages(user):
    cur_main.execute("SELECT * from MESSAGE WHERE von=?", (user,))
    return cur_main.fetchall()


def get_user_voice_time(user):
    cur_main.execute("SELECT minutes from VOICE WHERE user=?", (str(user),))
    data = cur_main.fetchall()
    return data[0][0] if data else 0


def get_user_trashtalk(guild_id, user):
    cur_main.execute(f"SELECT * FROM TrashTalk WHERE server=? AND von=?", [str(guild_id), str(user)])
    return cur_main.fetchall()


async def get_user_invites(guild_id, user, ctx=0):
    cur_main.execute("SELECT * FROM INVITES WHERE server=? AND von=?", ([str(guild_id), str(user)]))

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
    cur_main.execute('CREATE TABLE IF NOT EXISTS CONFIG ( SERVER TEXT, SPRACHE TEXT, PREFIX TEXT,'
                     ' MESSAGE_CHANNEL TEXT, WELCOME_TEXT TEXT, WELCOME_ROLE TEXT,'
                     ' WELCOME_CHANNEL TEXT, DISABLED_COMMANDS TEXT, TWITCH_USERNAME TEXT)')
    conn_main.commit()


def log_message(server, date, message):
    sql = "INSERT INTO MESSAGE (server, datum, von, nachricht) VALUES (?, ?, ?, ?)"
    val_1 = (server, date, str(message.author), str(message.content))

    cur_main.execute(sql, val_1)
    conn_main.commit()

    return 1
