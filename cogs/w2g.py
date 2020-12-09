from discord.ext import commands
import requests
import json

class w2g(commands.Cog):
    def __init__(self, bot):
        pass
    
    @commands.command()
    async def w2g(self, ctx, url):
        headers = {"share": url}
        yt = requests.post("https://w2g.tv/rooms/create.json", data=headers)
        await ctx.send("https://w2g.tv/rooms/" + json.loads(yt.content.decode())["streamkey"])

def setup(bot):
    bot.add_cog(w2g(bot))