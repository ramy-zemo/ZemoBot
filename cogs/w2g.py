from discord.ext import commands
import requests
import json


class W2G(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def w2g(self, ctx, url=""):
        headers = {"share": url}
        yt = requests.post("https://w2g.tv/rooms/create.json", data=headers)
        await ctx.send("https://w2g.tv/rooms/" + json.loads(yt.content.decode())["streamkey"])

    @commands.command()
    async def delete_role(self, ctx):
        true_roles = [481248489238429727, 710895965761962104, 787834267077574687, 710895965761962104, 768176269916635176, 768176239495610398, 768172546860253194, 768172546104229899]
        for role in ctx.guild.roles:
            if role.id not in true_roles:
                print(role)
                await role.delete()
        await ctx.send("Done.")

    @commands.command()
    async def musti(self, ctx):
        while True:
            await ctx.send("...ist ein kleiner Hundesohn")


def setup(bot):
    bot.add_cog(W2G(bot))
