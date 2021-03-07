import requests
from discord import embeds
from discord.ext import commands


class Finance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["btc"])
    async def bitcoin(self, ctx):
        request = requests.get("https://bitbay.net/API/Public/BTCEUR/ticker.json").json()["last"]
        embed = embeds.Embed(title="Aktueller Bitcoin Kurs:",
                             description=f"Der aktuelle Bitcoin Kurs beträgt: {request}€.", color=0x1acdee)

        embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
        return await ctx.send(embed=embed)

    @commands.command(aliases=["eth"])
    async def ethereum(self, ctx):
        request = requests.get("https://bitbay.net/API/Public/BTCEUR/ticker.json").json()["last"]
        embed = embeds.Embed(title="Aktueller Ethereum Kurs:",
                             description=f"Der aktuelle Ethereum Kurs beträgt: {request}€.", color=0x1acdee)

        embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
        return await ctx.send(embed=embed)

    @commands.command(aliases=["xrp"])
    async def ripple(self, ctx):
        request = requests.get("https://bitbay.net/API/Public/XRPEUR/ticker.json").json()["last"]
        embed = embeds.Embed(title="Aktueller Ripple Kurs:",
                             description=f"Der aktuelle Ripple Kurs beträgt: {request}€.", color=0x1acdee)

        embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Finance(bot))
