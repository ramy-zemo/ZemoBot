from discord.ext import commands, tasks
from dotenv import load_dotenv
from etc.ask import ask_for_thumbs
from etc.global_functions import get_main_channel
import sqlite3
import requests
import json
import discord
import asyncio
import os

load_dotenv()


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()
        self.username = ""
        self.done_notifiys = {}
        self.token = os.getenv('TWITCH_Authorization')
        self.twitch_loop.start()

    @tasks.loop(seconds=10.0)
    async def twitch_loop(self):
        await asyncio.sleep(5)
        self.cur_main.execute('SELECT SERVER, TWITCH_USERNAME FROM CONFIG')
        to_check = self.cur_main.fetchall()

        for x in to_check:
            guild_id = x[0]
            self.username = x[1]
            data = await self.get_data()
            if not data:
                return
            if data['is_live'] and self.username not in self.done_notifiys:
                await self.twitch_notify(int(guild_id))
                self.done_notifiys[self.username] = True
            elif not data['is_live'] and self.username in self.done_notifiys:
                del self.done_notifiys[self.username]
                del self.done_notifiys[self.username]

    @commands.command()
    async def frog(self, ctx):
        x = await ask_for_thumbs(self.bot, ctx, "", "Wie gehts?")
        print("X = ", x)

    @commands.is_owner()
    @commands.command()
    async def setup_twitch(self, ctx):
        self.cur_main.execute('SELECT TWITCH_USERNAME FROM CONFIG WHERE SERVER = ?', ([ctx.guild.id]))
        twitch_in_db = self.cur_main.fetchall()

        if twitch_in_db[0][0]:
            x = await ask_for_thumbs(self.bot, ctx, "Twitch bereits verknüpft", f"Der Server {ctx.guild} ist bereits mit dem Twitch Konto `{twitch_in_db[0][0]}` verbunden.\nMöchtest du ein neues verbinden?")

            if not x:
                return

        await ctx.send("Gib bitte den Nutzernamen des Twitchkontos an:")

        def check(reaction):
            if str(reaction.author) == str(self.bot.user):
                return False
            else:
                return True

        reaction = await self.bot.wait_for('message', check=check)
        self.username = reaction.content

        self.cur_main.execute('UPDATE CONFIG SET TWITCH_USERNAME = ? WHERE SERVER = ?', (self.username, str(ctx.guild.id)))
        self.conn_main.commit()

        if await self.get_data():
            await ctx.send(f'Das Twitch Konto {self.username} wurde erfolgreich mit dem Server {ctx.guild} verbunden.')
        else:
            return await ctx.send('Ungültiger Twitch Nutzername.\n')

    async def get_data(self):
        headers = {"client-id": os.getenv('TWITCH_CLIENT_ID'), "Authorization": f"Bearer {self.token}"}

        x = requests.get(f"https://api.twitch.tv/helix/search/channels?query={self.username}", headers=headers)

        try:
            data = json.loads(x.content.decode())["data"][0]
        except IndexError:
            return []

        try:
            return data if data['display_name'].lower() == self.username.lower() else []
        except:
            return []

    @commands.command()
    @commands.is_owner()
    async def twitch_notify(self, guild_id):
        data = await self.get_data()

        embed = discord.Embed(title=f"{data['display_name']} ist nun Online auf Twitch",
                              description=f"{data['title']}\n{f'https://www.twitch.tv/{self.username}'}\n",
                              url=f"https://www.twitch.tv/{self.username}",
                              color=0x9244ff)
        embed.set_thumbnail(url=data["thumbnail_url"])

        embed.set_author(name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

        guild = self.bot.get_guild(guild_id)
        channel = await get_main_channel(guild.id)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Twitch(bot))
