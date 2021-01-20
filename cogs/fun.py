from discord.ext import commands
import discord
from ZemoBot.etc.error_handling import invalid_argument
from requests import get
from dotenv import load_dotenv
import os
import bitlyshortener


load_dotenv()


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
    async def google(self, ctx, member: discord.Member, *args):
        url = str("https://lmgtfy.app/?q=" + '+'.join(args) + "&iie=1")

        if os.getenv("BITLY_API"):
            shortener = bitlyshortener.Shortener(tokens=[os.getenv("BITLY_API")], max_cache_size=256)
            short_url = shortener.shorten_urls([url])
            await ctx.send(member.mention + " " + short_url[0])

        else:
            await ctx.send(member.mention + " " + url)

        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Fun(bot))
