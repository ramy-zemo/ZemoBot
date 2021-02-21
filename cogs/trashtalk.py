from discord.ext import commands
from discord import Member
from datetime import date
from etc.sql_reference import get_user_trashtalk, log_trashtalk, reset_trashtalk


class Trashtalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trashtalk(self, ctx, member: Member):
        datum = str(date.today())
        result = get_user_trashtalk(ctx.guild.id, ctx.message.author)
        daten = [x[0] for x in result if x[0] == datum]

        if len(daten) < 10:
            with open("trashtalk.txt") as file:
                text = file.readlines()

                try:
                    for t in text:
                        await member.send(t)
                except:
                    return await ctx.send(f"Trashtalk an {member.mention} fehlgeschlagen.")

                log_trashtalk(ctx.guild.id, datum, ctx.message.author, member)
        else:
            await ctx.send(f"{ctx.message.author.mention} du hast dein Trash Limit für heute erreicht.")

    @commands.command()
    async def trashtalk_add(self, ctx, *args):
        with open("trashtalk.txt", "a") as file:
            file.write(" ".join(args) + "\n")

        await ctx.send("Nachricht erfolgreich hinzugefügt!")

    @commands.command()
    async def trashtalk_list(self, ctx):
        with open("trashtalk.txt", "r") as file:

            await ctx.message.author.send("```\n" + ''.join(file.readlines()) + "\n```")

    @commands.command()
    async def trashtalk_stats(self, ctx, member: Member = 0, *args):
        datum = str(date.today())
        if not member:
            result = get_user_trashtalk(ctx.guild.id, ctx.message.author)
        else:
            result = get_user_trashtalk(ctx.guild.id, member)

        today = [x[1] for x in result if x[1] == datum]

        if args:
            return len(result)
        else:
            await ctx.send(f"All time: {len(result)}, Today: {len(today)}")

    @commands.command()
    async def trashtalk_reset(self, ctx, *args):
        try:
            reset_trashtalk(ctx.guild.id, ctx.message.author)
            await ctx.send(f"Trashtalk für {ctx.message.author.mention} erfolgreich zurückgesetzt.")
        except:
            await ctx.send(f"Nutzer {ctx.message.author.mention} nicht gefunden.")


def setup(bot):
    bot.add_cog(Trashtalk(bot))
