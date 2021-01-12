from random import choice
from discord import File
from discord.ext import commands


class RandomPicker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coin(self, ctx):
        head_or_tail = choice([0, 1])
        if head_or_tail:
            await ctx.send(f"{ctx.message.author.mention} Zahl",
                           file=File('img/coin/Coin_Tail.gif', filename="Tail.gif"))
        else:
            await ctx.send(f"{ctx.message.author.mention} Kopf",
                           file=File('img/coin/Coin_Head.gif', filename="Head.gif"))

    @commands.command()
    async def pick_number(self, ctx, *args):
        start = int(args[0])
        end = int(args[1])
        await ctx.send(choice(range(start, end, 1)))


def setup(bot):
    bot.add_cog(RandomPicker(bot))