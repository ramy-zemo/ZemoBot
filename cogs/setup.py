from discord.ext import commands
from ZemoBot.etc.ask import ask
from ZemoBot.etc.sql_reference import change_prefix


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setup(self, ctx):
        asko = await ask(ctx.message.author, "reaction_add", "Möchtest du den Command Prefix (Standard $) ändern?",
                         ctx.message.channel, self.bot, max_answers=1, reaction_type="bool")

        if asko:
            prefix = await ask(ctx.message.author, "message", "Gib bitte den neuen Prefix ein:", ctx.message.channel,
                               self.bot, max_answers=1, msg_max_length=1,
                               msg_description="Wähle am besten ein Sonderzeichen.")

            change_prefix(ctx.guild.id, prefix)


def setup(bot):
    bot.add_cog(Setup(bot))
