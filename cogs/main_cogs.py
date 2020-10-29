from discord.ext import commands
import discord


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        with open("trashtalk.txt", encoding="utf-8") as file:
            self.text = file.readlines()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot {} läuft!".format(self.bot.user))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(
                'Selam {}, willkommen in der Familie!\n',
                'Hast du Ärger, gehst du Cafe Al Bustan, gehst du zu Arafat!'.format(member))

    @commands.command()
    async def trashtalk(self, ctx, user: discord.User):
        for t in self.text:
            await user.send(t)

    @commands.command()
    async def amo(self, ctx, *args):
        for m in ctx.guild.members:
            if m != ctx.message.author:
                for role in m.roles:
                    if "AMO" == role.name:
                        await m.send("{}".format(" ".join(args)))


def setup(bot):
    bot.add_cog(Basic(bot))
