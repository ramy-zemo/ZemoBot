import requests
import discord

from discord.ext import commands
from io import BytesIO
from PIL import Image


class Trump(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trump(self, ctx, *args):
        await ctx.send("```" + requests.get("https://www.tronalddump.io/random/quote").json()["value"] + " - Donald Trump" + "```")
    
    @commands.command()
    async def trump_img(self, ctx, *args):
        img = Image.open(BytesIO(requests.get("https://www.tronalddump.io/random/meme").content))

        with BytesIO() as output:
            img.save(output, format="PNG")
            output.seek(0)
            await ctx.send(file=discord.File(fp=output, filename="image.png"))


def setup(bot):
    bot.add_cog(Trump(bot))
