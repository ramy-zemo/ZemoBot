import requests
from discord import embeds
from discord.ext import commands


class Finance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["btc"])
    async def bitcoin(self, ctx):
        currency_rate = requests.get("https://bitbay.net/API/Public/BTCEUR/ticker.json").json()["last"]
        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        title = self.bot.language(self.bot, lang, "FINANCE_CURRENCY_RATE_TITLE", currency="Bitcoin")

        description = self.bot.language(self.bot, lang, "FINANCE_CURRENCY_RATE_DESCRIPTION",
                                        currency="Bitcoin", currency_rate=currency_rate)

        embed = embeds.Embed(title=title, description=description, color=0x1acdee)

        embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
        return await ctx.send(embed=embed)

    @commands.command(aliases=["eth"])
    async def ethereum(self, ctx):
        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        currency_rate = requests.get("https://bitbay.net/API/Public/BTCEUR/ticker.json").json()["last"]

        title = self.bot.language(self.bot, lang, "FINANCE_CURRENCY_RATE_TITLE",
                                  currency="Ethereum")

        description = self.bot.language(self.bot, lang, "FINANCE_CURRENCY_RATE_DESCRIPTION",
                                        currency="Ethereum", currency_rate=currency_rate)

        embed = embeds.Embed(title=title, description=description, color=0x1acdee)

        embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
        return await ctx.send(embed=embed)

    @commands.command(aliases=["xrp"])
    async def ripple(self, ctx):
        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        currency_rate = requests.get("https://bitbay.net/API/Public/XRPEUR/ticker.json").json()["last"]

        title = self.bot.language(self.bot, lang, "FINANCE_CURRENCY_RATE_TITLE",
                                  currency="Ripple")

        description = self.bot.language(self.bot, lang, "FINANCE_CURRENCY_RATE_DESCRIPTION",
                                        currency="Ripple", currency_rate=currency_rate)

        embed = embeds.Embed(title=title, description=description, color=0x1acdee)

        embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Finance(bot))
