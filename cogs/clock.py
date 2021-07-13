import asyncio

from discord.ext import commands


class Clock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timers = {}

    @commands.command()
    async def timer(self, ctx, minutes):
        lang = self.bot.guild_languages.get(ctx.guild.id)
        timer_end = self.bot.language(self.bot, lang, "CLOCK_TIMER_END")
        timer_already_running = self.bot.language(self.bot, lang, "TIMER_ALREADY_RUNNING")

        if ctx.message.author in self.timers:
            return await ctx.send(timer_already_running)

        await asyncio.sleep(int(minutes) * 60)
        for msg in range(3):
            await ctx.message.author.send(":alarm_clock:" * 10 + timer_end + ":alarm_clock:" * 10)


def setup(bot):
    bot.add_cog(Clock(bot))
