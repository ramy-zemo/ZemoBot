from discord.ext import commands
from etc.ask import ask
import sqlite3


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()

    @commands.command()
    async def setup(self, ctx):
        asko = await ask(ctx.message.author, "reaction_add", "Möchtest du den Command Prefix (Standard $) ändern?",
                         ctx.message.channel, self.bot, max_answers=1, reaction_type="bool")

        print(asko)


def setup(bot):
    bot.add_cog(Setup(bot))
