from discord.ext import commands
from discord import Member
from datetime import date
from sql.trashtalk_log import get_user_trashtalk, log_trashtalk, reset_trashtalk
from sql.trashtalk import get_trashtalk, add_trashtalk


class Trashtalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trashtalk(self, ctx, member: Member):
        datum = str(date.today())
        result = get_user_trashtalk(ctx.guild.id, ctx.message.author.id)
        daten = [x[0] for x in result if x[0] == datum]

        if len(daten) < 10:
            messages = get_trashtalk(ctx.guild.id)
            try:
                for msg in messages:
                    await member.send(msg)
            except:
                return await ctx.send(f"Trashtalk an {member.mention} fehlgeschlagen.")

            log_trashtalk(ctx.guild.id, datum, ctx.message.author.id, member.id)
        else:
            await ctx.send(f"{ctx.message.author.mention} du hast dein Trash Limit für heute erreicht.")

    @commands.command()
    async def trashtalk_add(self, ctx, *args):
        add_trashtalk(ctx.guild.id, str(date.today()), ctx.message.author.id, " ".join(args))
        await ctx.send("Nachricht erfolgreich hinzugefügt!")

    @commands.command()
    async def trashtalk_list(self, ctx):
        messages = get_trashtalk(ctx.guild.id)

        if messages:
            await ctx.message.author.send("```\n" + '\n'.join(messages) + "\n```")
        else:
            await ctx.message.author.send("Aktuell sind leider keine Daten für diesen Server vorhanden.")

    @commands.command()
    async def trashtalk_stats(self, ctx, member: Member = 0, *args):
        datum = str(date.today())
        if not member:
            result = get_user_trashtalk(ctx.guild.id, ctx.message.author.id)
        else:
            result = get_user_trashtalk(ctx.guild.id, member.id)

        today = [x[1] for x in result if x[1] == datum]

        if args:
            return len(result)
        else:
            await ctx.send(f"All time: {len(result)}, Today: {len(today)}")

    @commands.command()
    async def trashtalk_reset(self, ctx, *args):
        try:
            reset_trashtalk(ctx.guild.id, ctx.message.author.id)
            await ctx.send(f"Trashtalk für {ctx.message.author.mention} erfolgreich zurückgesetzt.")
        except:
            await ctx.send(f"Nutzer {ctx.message.author.mention} nicht gefunden.")


def setup(bot):
    bot.add_cog(Trashtalk(bot))
