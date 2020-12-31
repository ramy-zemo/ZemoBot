from discord.ext import commands
from etc.error_handling import invalid_argument
from random import choice
from discord import File
import os


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, *args):
        if not args:
            await ctx.send(ctx.author.avatar_url)
        elif len(args) == 1:
            await ctx.send(ctx.guild.get_member(int(str(args[0]).strip("<>!@"))).avatar_url)
        else:
            return await invalid_argument(ctx, "avatar", "$avatar @Member")

    @commands.command()
    async def coin(self, ctx):
        head_or_tail = choice([0, 1])
        if head_or_tail:
            await ctx.send(f"{ctx.message.author.mention} Zahl", file=File('img/coin/Coin_Tail.gif', filename="Tail.gif"))
        else:
            await ctx.send(f"{ctx.message.author.mention} Kopf", file=File('img/coin/Coin_Head.gif', filename="Head.gif"))

    @commands.is_owner()
    @commands.command()
    async def kick(self, ctx, *args):
        to_kick = ctx.guild.get_member(int(str(args[0]).strip("<>!@")))
        await ctx.guild.kick(to_kick)
        await ctx.send("Habebe ist erledigt")


def setup(bot):
    bot.add_cog(Fun(bot))
