import requests

from discord.ext import commands
from discord import Embed
from bs4 import BeautifulSoup


class FaceitFinder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def faceit_finder(self, ctx, url):
        lang = self.bot.guild_languages.get(ctx.guild.id)
        faceit_finder_title = self.bot.language(self.bot, lang, "FACEIT_FINDER_TITLE")
        faceit_finder_account_not_found = self.bot.language(self.bot, lang, "FACEIT_NO_ACCOUNT_FOUND")
        faceit_finder_account_field = self.bot.language(self.bot, lang, "FACEIT_FINDER_ACCOUNT_FIELD")

        try:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
            }

            response = requests.post('https://faceitfinder.com/profile/', headers=headers, data={'name': url})

            faceit_id = ''.join([x for x in response.content.decode() if x.isdigit()])

            response_html = requests.get('https://faceitfinder.com/profile/' + faceit_id, headers=headers)

            response_html_soup = BeautifulSoup(response_html.content, 'html.parser')
            url = response_html_soup.find_all("a", href=True)

            faceit_url = [x["href"] for x in url if "https://www.faceit.com/" in str(x["href"]) and "csgo" not in str(x["href"])][0]
            faceit_description = response_html_soup.find_all("meta")[::-1][0]["content"]
            skill_image_url = "https://faceitfinder.com" + [x["src"] for x in response_html_soup.find_all("img") if "skill_level" in str(x["src"])][0]

            embed = Embed(title=faceit_finder_title, description=faceit_description, color=0x1acdee)

            embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)

            embed.add_field(name=faceit_finder_account_field, value=faceit_url)
            embed.set_thumbnail(url=skill_image_url)

            await ctx.send(embed=embed)

        except:
            embed = Embed(title=faceit_finder_title, description=faceit_finder_account_not_found, color=0x1acdee)
            embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)

            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FaceitFinder(bot))
