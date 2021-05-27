import requests
import html

from bs4 import BeautifulSoup
from discord.ext import commands
from random import choice
from etc.error_handling import invalid_argument


class Font(commands.Cog):
    def __init__(self, bot):
        self.font_list = ['3-d', '3x5', '5lineoblique ', 'acrobatic', 'alligator', 'alligator2', 'alphabet', 'avatar',
                     'banner', 'banner3-D', 'banner3', 'banner4', 'barbwire', 'basic', 'bell', 'big', 'bigchief',
                     'binary', 'block', 'bubble', 'bulbhead', 'calgphy2', 'caligraphy', 'catwalk', 'chunky', 'coinstak',
                     'colossal', 'computer', 'contessa', 'contrast', 'cosmic', 'cosmike', 'cyberlarge', 'cybermedium',
                     'cybersmall', 'cygnet', 'diamond', 'digital', 'doh', 'doom', 'dotmatrix', 'drpepper', 'eftichess',
                     'eftifont', 'eftipiti', 'eftirobot', 'eftitalic ', 'eftiwall', 'eftiwater', 'epic', 'fender',
                     'fourtops', 'fuzzy', 'goofy', 'gothic', 'graffiti', 'hollywood',
                     'invita', 'isometric1', 'isometric2', 'isometric3', 'isometric4', 'italic', 'jazmine', 'kban',
                     'larry3d', 'lcd', 'lean', 'letters', 'linux', 'lockergnome', 'madrid', 'marquee', 'maxfour',
                     'mike', 'mini', 'mirror', 'nancyj-fancy', 'nancyj-underlined', 'nancyj', 'nipples', 'o8', 'ogre',
                     'pawp', 'peaks', 'pebbles', 'pepper', 'poison', 'puffy', 'pyramid', 'rectangles', 'relief',
                     'relief2', 'rev', 'roman', 'rot13', 'rounded', 'rowancap', 'rozzo', 'sblood', 'script', 'serifcap',
                     'shadow', 'short', 'slant', 'slide', 'slscript', 'small', 'smisome1', 'smkeyboard', 'smscript',
                     'smshadow', 'smslant', 'smtengwar', 'speed', 'stampatello', 'standard', 'starwars', 'stellar',
                     'stop', 'straight', 'swan', 'tanja', 'tengwar', 'term', 'thick', 'thin', 'threepoint', 'ticks',
                     'ticksslant', 'tinker-toy', 'tombstone', 'trek', 'twopoint', 'univers', 'usaflag', 'weird']
        self.bot = bot

    @commands.command()
    async def font_list(self, ctx):
        await ctx.message.author.send("```" + "\n".join(self.font_list) + "```")

    @commands.command()
    async def font(self, ctx, keyword=None, font=None,):
        if not keyword:
            return await invalid_argument(self, ctx, "font")

        if not font:
            font = choice(self.font_list)

        url = "http://www.network-science.de/ascii/ascii.php"
        request = requests.get(url + f"?TEXT={keyword}&x=30&y=11&FONT={font}&RICH=no&FORM=left&STRE=no&WIDT=80")

        soup = BeautifulSoup(request.content, "html.parser")

        text = html.unescape(str(soup.find_all("pre")[1]))

        text_ascii = "\n".join(text.split("\n")[1:-1])

        text_discord = "```\n" + text_ascii + f"\n\nFont: {font}, Keyword: {keyword}" + "```"

        await ctx.send(text_discord)


def setup(bot):
    bot.add_cog(Font(bot))
