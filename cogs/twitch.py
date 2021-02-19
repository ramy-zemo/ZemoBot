from discord.ext import commands, tasks
from dotenv import load_dotenv
from etc.ask import ask_for_thumbs
from etc.sql_reference import get_main_channel, update_twitch_username, get_twitch_username, get_all_twitch_data
import requests
import json
import discord
import asyncio
import os

load_dotenv()


class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.username = ""
        self.done_notifiys = {}
        self.twitch_loop.start()

    @tasks.loop(seconds=5.0)
    async def twitch_loop(self):
        await asyncio.sleep(5)
        to_check = get_all_twitch_data()

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
        token_req = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={os.getenv('TWITCH_CLIENT_ID')}&client_secret={os.getenv('TWITCH_CLIENT_SECRET')}&grant_type=client_credentials")
        token = json.loads(token_req.content.decode())["access_token"]
        headers = {"client-id": os.getenv('TWITCH_CLIENT_ID'), "Authorization": f"Bearer {token}"}

        x = requests.get(f"https://api.twitch.tv/helix/search/channels?query={self.username}", headers=headers)

        try:
            data = [x for x in json.loads(x.content.decode())["data"] if x["broadcaster_login"].lower() == self.username.lower()][0]
        except IndexError:
            return []

        try:
            return data if data['display_name'].lower() == self.username.lower() else []
        except:
            return []

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
