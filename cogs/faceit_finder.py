import requests
from discord.ext import commands
from discord import Embed
from bs4 import BeautifulSoup


class Faceit_finder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def faceit_finder(self, ctx, url):
        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            }

            data = {
                'name': url
            }

            response = requests.post('https://faceitfinder.com/profile/', headers=headers, data=data)

            faceit_id = ''.join([x for x in response.content.decode() if x.isdigit()])

            response_html = requests.get('https://faceitfinder.com/profile/' + faceit_id, headers=headers)

            response_html_soup = BeautifulSoup(response_html.content, 'html.parser')
            url = response_html_soup.find_all("a", href=True)

            faceit_url = \
            [x["href"] for x in url if "https://www.faceit.com/" in str(x["href"]) and "csgo" not in str(x["href"])][0]
            faceit_description = response_html_soup.find_all("meta")[::-1][0]["content"]

            embed = Embed(title="Faceit Finder",
                          description=faceit_description,
                          color=0x1acdee)

            embed.set_author(name="Zemo Bot",
                             icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

            embed.add_field(name="Faceit Account:", value=faceit_url)

            await ctx.send(embed=embed)
        except:
            await ctx.send("Faceit Account konnte nicht gefunden werden.")


def setup(bot):
    bot.add_cog(Faceit_finder(bot))
