import requests
from discord.ext import commands

class Meme(commands.Cog):
    def __init__(self, bot):
        pass

    @commands.command()
    async def meme(self, ctx, *args):
        try:
            await ctx.send(requests.get("https://meme-api.herokuapp.com/gimme").json()["url"])
        except:
            await ctx.send("Die Meme API ist aktuell nicht verfügbar.")

def setup(bot):
    bot.add_cog(Meme(bot))