from discord.ext import commands
from datetime import date
import sqlite3

class Trashtalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        with open("trashtalk.txt") as file:
                    self.text = file.readlines()
        
        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()

    @commands.command()
    async def trashtalk(self, ctx, *args):
        datum = str(date.today())

        sql = f"SELECT * FROM TrashTalk WHERE von=?"

        self.cur_main.execute(sql, ([str(ctx.message.author)]))

        result = self.cur_main.fetchall()
        daten = [x[0] for x in result if x[0] == datum]

        if len(daten) < 10:
            users_to_tt = [ctx.message.guild.get_member(int(str(x).strip("<>!@"))) for x in args]
            for user in users_to_tt:
                try:
                    for t in self.text:
                        await user.send(t)
                except:
                    return await ctx.send(f"Trashtalk an {user.mention} fehlgeschlagen.")

                sql = "INSERT INTO TrashTalk (server, datum, von, an) VALUES (?, ?, ?, ?)"
                val_1 = (str(ctx.guild.id), datum, str(ctx.message.author), str(user))

                self.cur_main.execute(sql,val_1)
                self.conn_main.commit()
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
    async def trashtalk_stats(self, ctx, *args):
        datum = str(date.today())
        try:
            sql = f"SELECT * FROM TrashTalk WHERE server=? AND von=?"
            val = ([str(ctx.guild.id), str(ctx.message.author)])
            self.cur_main.execute(sql, val)

            result = self.cur_main.fetchall()
            daten = [x[1] for x in result if x[1] == datum]

            if args:
                return len(result)
            else:
                await ctx.send(f"All time: {len(result)}, Today: {len(daten)}")

        except sqlite3.OperationalError:
            await ctx.send("Bisher sind keine Daten vorhanden.")

    @commands.command()
    async def trashtalk_reset(self, ctx, *args):
        try:
            self.cur_main.execute(f"DELETE FROM TrashTalk WHERE server=? AND von=?", (str(ctx.guild.id), str(ctx.message.author)))
            self.conn_main.commit()
            await ctx.send(f"Trashtalk für {ctx.message.author.mention} erfolgreich zurückgesetzt.")
        except:
            await ctx.send(f"Nutzer {ctx.message.author.mention} nicht gefunden.")


def setup(bot):
    bot.add_cog(Trashtalk(bot))
