from discord.ext import commands


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def delete(self, ctx):
        await self.delete_role(ctx)
        await self.delete_channel(ctx)

    @commands.command()
    async def delete_role(self, ctx):
        true_roles = [481248489238429727, 710895965761962104, 787834267077574687, 710895965761962104, 768176269916635176, 768176239495610398, 768172546860253194, 768172546104229899]
        for role in ctx.guild.roles:
            if role.id not in true_roles:
                try:
                    await role.delete()
                except Exception as e:
                    pass

        await ctx.send("Done.")

    @commands.command()
    async def delete_channel(self, ctx):
        true_channels = [768172543273730058, 768175708799107192, 768176881735696384, 768177068630212648, 768177563633713242, 768177809801609275, 768177845264056359, 768177889891188757, 768179070751735818, 768179163919679548, 768179253883306035, 768179505595940874, 768179640765906964, 769921393281466408, 769921717887172608, 769922292297367603]

        for channel in ctx.guild.channels:
            if channel.id not in true_channels:
                try:
                    await channel.delete()
                except:
                    pass
        await ctx.send("Done.")

    @commands.command()
    async def show_roles(self, ctx):
        for role in ctx.guild.roles:
            print(role, role.id)

    @commands.command()
    async def show_channels(self, ctx):
        for channel in ctx.guild.channels:
            print(channel, channel.id)


def setup(bot):
    bot.add_cog(Debug(bot))
