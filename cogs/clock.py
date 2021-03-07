import requests
import asyncio

from discord.ext import commands
from discord import Embed
from bs4 import BeautifulSoup


class Clock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.timers ={}

    @commands.command()
    async def timer(self, ctx, minutes):
        if ctx.message.author in self.timers:
            return await ctx.send("")

        await asyncio.sleep(int(minutes) * 60)
        for msg in range(3):
            await ctx.message.author.send(f":alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock:\n:alarm_clock::alarm_clock: Dein {minutes} Minuten Timer ist vorbei. :alarm_clock::alarm_clock:\n:alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock::alarm_clock:")


def setup(bot):
    bot.add_cog(Clock(bot))
