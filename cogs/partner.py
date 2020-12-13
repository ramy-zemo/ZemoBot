from discord.ext import commands
import sqlite3

class partner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()

    @commands.command()
    async def partner(self, ctx):
        print("Test")

def setup(bot):
    bot.add_cog(partner(bot))