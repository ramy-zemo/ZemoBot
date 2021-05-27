from discord.ext import commands
from discord import Member
from datetime import date


class Trashtalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trashtalk(self, ctx, member: Member):
        datum = str(date.today())
        result = self.bot.ApiClient.request(self.bot.ApiClient.get_user_trashtalk,
                                            params={"guild_id": ctx.guild.id,
                                                    "user_id": ctx.message.author.id})
        daten = [x[0] for x in result if x[0] == datum]

        if len(daten) < 3:
            messages = self.bot.ApiClient.request(self.bot.ApiClient.get_trashtalk, params={"guild_id": ctx.guild.id})
            if messages:
                try:
                    for msg in messages:
                        await member.send(msg)
                except:
                    return await ctx.send(f"Trashtalk an {member.mention} fehlgeschlagen.")

            else:
                return await ctx.send(f"Für den Server {ctx.guild} sind aktuell keine Trashtalk Nachrichten vorhanden.")

            self.bot.ApiClient.request(self.bot.ApiClient.log_trashtalk,
                                       params={"guild_id": ctx.guild.id,
                                               "datum": datum,
                                               "from_user_id": ctx.message.author.id,
                                               "to_user_id": member.id})
        else:
            await ctx.send(f"{ctx.message.author.mention} du hast dein Trash Limit für heute erreicht.")

    @commands.command()
    async def trashtalk_add(self, ctx, *args):
        self.bot.ApiClient.request(self.bot.ApiClient.add_trashtalk,
                                   params={"guild_id": ctx.guild.id,
                                           "added_on": str(date.today()),
                                           "added_by_user_id": ctx.message.author.id,
                                           "message": " ".join(args)})

        await ctx.send("Nachricht erfolgreich hinzugefügt!")

    @commands.command()
    async def trashtalk_list(self, ctx):
        messages = self.bot.ApiClient.request(self.bot.ApiClient.get_trashtalk, params={"guild_id": ctx.guild.id})

        if messages:
            await ctx.message.author.send("```\n" + '\n'.join(messages) + "\n```")
        else:
            await ctx.message.author.send("Aktuell sind leider keine Daten für diesen Server vorhanden.")

    @commands.command()
    async def trashtalk_stats(self, ctx, member: Member = 0, *args):
        datum = str(date.today())
        if not member:
            result = self.bot.ApiClient.request(self.bot.ApiClient.get_user_trashtalk,
                                                params={"guild_id": ctx.guild.id,
                                                        "user_id": ctx.message.author.id})
        else:
            result = self.bot.ApiClient.request(self.bot.ApiClient.get_user_trashtalk,
                                                params={"guild_id": ctx.guild.id,
                                                        "user_id": member.id})

        today = [x[1] for x in result if x[1] == datum]

        if args:
            return len(result)
        else:
            await ctx.send(f"All time: {len(result)}, Today: {len(today)}")

    @commands.command()
    async def trashtalk_reset(self, ctx, *args):
        try:
            self.bot.ApiClient.request(self.bot.ApiClient.reset_user_trashtalk,
                                       params={"guild_id": ctx.guild.id, "user_id": ctx.message.author.id})
            await ctx.send(f"Trashtalk für {ctx.message.author.mention} erfolgreich zurückgesetzt.")
        except:
            await ctx.send(f"Nutzer {ctx.message.author.mention} nicht gefunden.")


def setup(bot):
    bot.add_cog(Trashtalk(bot))
