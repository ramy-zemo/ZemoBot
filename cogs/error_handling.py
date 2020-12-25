from discord.ext import commands
import discord
from discord.ext.commands import CommandNotFound


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def invalid_argument(self, ctx, command, usage):
        embed = discord.Embed(title="Ungültige Parameter",
                              description=f"Die Werte die du an den Command `{command}` übergeben hast sind ungültig.",
                              color=0x1acdee)
        embed.add_field(name=f"Richtigen Parameter:", value=f"{usage}", inline=True)

        embed.set_author(name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        embed.set_footer(text="Reagiere auf diese Nachricht um die Einladung annzunehmen.")
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(":question: Unbekannter Befehl :question:")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
