from discord.ext import commands, tasks
from dotenv import load_dotenv
from etc.ask import ask_for_thumbs
from etc.sql_reference import get_main_channel, update_twitch_username, get_twitch_username, get_all_twitch_data
import requests
import json
import discord
import asyncio
import os
from time import sleep


load_dotenv()


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.username = ""
        self.done_notifications = {}
        self.twitch_loop.start()
        self.get_twitch_token()

    def get_twitch_token(self):
        token_req = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={os.getenv('TWITCH_CLIENT_ID')}&client_secret={os.getenv('TWITCH_CLIENT_SECRET')}&grant_type=client_credentials")
        self.token = json.loads(token_req.content.decode())["access_token"]

    @tasks.loop(seconds=5.0)
    async def twitch_loop(self):
        to_check = get_all_twitch_data()

        for guild_data in to_check:
            guild_id = guild_data[0]

            if guild_data[1]:
                self.username = guild_data[1]
            else:
                continue

            data = await self.get_data()
            if not data:
                return
            if data['is_live'] and self.username not in self.done_notifications:
                await self.twitch_notify(int(guild_id))
                self.done_notifications[self.username] = True
            elif not data['is_live'] and self.username in self.done_notifications:
                del self.done_notifications[self.username]

    @commands.is_owner()
    @commands.command()
    async def setup_twitch(self, ctx):
        twitch_in_db = get_twitch_username(ctx.guild.id)

        if twitch_in_db:
            x = await ask_for_thumbs(self.bot, ctx, "Twitch bereits verknüpft", f"Der Server {ctx.guild} ist bereits mit dem Twitch Konto `{twitch_in_db}` verbunden.\nMöchtest du ein neues verbinden?")

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

        update_twitch_username(ctx.guild.id, self.username)

        if await self.get_data():
            await ctx.send(f'Das Twitch Konto {self.username} wurde erfolgreich mit dem Server {ctx.guild} verbunden.')
        else:
            return await ctx.send('Ungültiger Twitch Nutzername.\n')

    async def get_data(self):
        headers = {"client-id": os.getenv('TWITCH_CLIENT_ID'), "Authorization": f"Bearer {self.token}"}

        channel_query = requests.get(f"https://api.twitch.tv/helix/search/channels?query={self.username}", headers=headers)

        if channel_query.status_code == 200:
            try:
                data = [x for x in json.loads(channel_query.content.decode())["data"] if x["broadcaster_login"].lower() == self.username.lower()][0]
            except IndexError:
                return []

            try:
                return data if data['display_name'].lower() == self.username.lower() else []
            except:
                return []
        else:
            self.get_twitch_token()

    async def twitch_notify(self, guild_id):
        data = await self.get_data()

        embed = discord.Embed(title=f"{data['display_name']} ist nun Live auf Twitch",
                              description=f"{data['title']}\n{f'https://www.twitch.tv/{self.username}'}\n",
                              url=f"https://www.twitch.tv/{self.username}",
                              color=0x9244ff)
        embed.set_thumbnail(url=data["thumbnail_url"])

        embed.set_author(name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        channel = await get_main_channel(self.bot.get_guild(guild_id))
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Twitch(bot))
