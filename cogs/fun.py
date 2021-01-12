from discord.ext import commands
from etc.error_handling import invalid_argument


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


def setup(bot):
    bot.add_cog(Fun(bot))
