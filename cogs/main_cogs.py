from discord.ext import commands
import discord
import asyncio
from datetime import date
import random
import requests
import sqlite3
import string
from time import perf_counter
import json
from bs4 import BeautifulSoup
import html
from .ranking import Ranking


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.invites = {}
        
        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()

        self.voice_track = {}

        self.trashtalk = self.bot.get_cog("Trashtalk")
        self.ranking = Ranking(bot)

    @commands.command()
    async def amo(self, ctx, *args):
        y = [mem for mem in [m for m in ctx.guild.members if m != ctx.message.author] if
             "AMO" in [x.name for x in mem.roles]]

        for x in y:
            await x.send("{}".format(" ".join(args)))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong!  :ping_pong:  In {round(self.bot.latency * 1000)}ms')

def setup(bot):
    bot.add_cog(Basic(bot))
