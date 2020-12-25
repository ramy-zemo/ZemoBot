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
        cur_main.execute("SELECT * FROM CHANNELS WHERE server=?", ([guild.id]))
        channel_id = cur_main.fetchall()[0][1]
        channel = discord.utils.get(guild.channels, id=int(channel_id))

    except IndexError:
        channel = discord.utils.get(guild.channels, name="zemo-bot")

    return channel


async def ask_for_thumbs(bot, ctx, title, question):
    embed = discord.Embed(title=title,
                          description=question,
                          color=0x1acdee)

    embed.set_author(name="Zemo Bot",
                     icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
    embed.set_footer(text="Reagiere auf diese Nachricht um diese Frage zu beantworten.")

    request = await ctx.send(embed=embed)

    for emoji in ('👍', '👎'):
        await request.add_reaction(emoji)

    def check(reaction, author):
        return str(reaction.emoji) in ['👍', '👎'] and str(author) != str(bot.user) and str(author) == str(ctx.message.author)

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)

    except asyncio.TimeoutError:
        await ctx.send("Deine Antwort hat zu lange gedauert.")
        return False

    return reaction.emoji == '👍'