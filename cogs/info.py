from discord.ext import commands
import sqlite3
import discord

class info(commands.Cog):
    def __init__(self, bot):
        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()
        self.bot = bot

    @commands.command()
    async def info(self, ctx, *args):

        self.cur_main.execute("SELECT * from MESSAGE WHERE von=?", ([str(ctx.author)]))
        messages = len(self.cur_main.fetchall())

        self.cur_main.execute("SELECT minutes from VOICE WHERE user=?", ([str(ctx.author)]))
        minutes = self.cur_main.fetchall()[0][0]

        self.cur_main.execute(f"SELECT * FROM TrashTalk WHERE server=? AND von=?", [str(ctx.guild.id), str(ctx.message.author)])
        trashtalk = len(self.cur_main.fetchall())

        embed = discord.Embed(title="Info", description="Deine Nutzerinformationen:", color=0x1acdee)
        embed.add_field(name="Nachrichten", value=f"Du hast bisher {messages} Nachrichten versendet.", inline=False)
        embed.add_field(name="Invites", value=f"""Du hast bisher {await self.invite(ctx, "No Print")} Invites versendet.""", inline=False)
        embed.add_field(name="Minuten", value=f"Du warst {minutes} Minuten mit einem Sprachchannel verbunden.", inline=False)
        embed.add_field(name="Trashtalk", value=f"""Du hast bereits {trashtalk} mal Trashtalk versendet.""", inline=False)
        embed.set_author(name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *args):
        embed = discord.Embed(title="Help", description="List of available commands", color=0x1acdee)
        embed.set_author(
            name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        embed.add_field(name="$trashtalk (*Mention)", value="Trashtalk people", inline=False)
        embed.add_field(name="$trashtalk_stats", value="Show your Discord Trashtalk Stats", inline=False)
        embed.add_field(name="$trashtalk_reset", value="Reset your Trashtalk Stats", inline=False)
        embed.add_field(name="$trashtalk_list", value="Show Trashtalk Words", inline=False)
        embed.add_field(name="$trashtalk_add", value="Add Words to trashtalk", inline=False)
        embed.add_field(name="$mafia (*mention)", value="Start Mafia Game", inline=False)
        embed.add_field(name="$ping", value="Check if bot is alive", inline=False)
        embed.add_field(name="$stats", value="Get your statistics", inline=False)
        embed.add_field(name="$auszeit (*mention) (*seconds)", value="Timeout Users", inline=False)
        embed.add_field(name="$meme", value="Return random meme", inline=False)
        embed.add_field(name="$font (*keyword) (font)", value="Returns ASCII Art, from provided Text.", inline=False)
        embed.add_field(name="$font_list", value="Get List of available Fonts.", inline=False)
        embed.add_field(name="$invite", value="List of your successful invites.", inline=False)
        embed.add_field(name="$w2g (url)", value="Create watch2gether room with provided Link.", inline=False)
        embed.add_field(name="$info", value="Get your Userinformation.", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self, ctx, *args):
        self.cur_main.execute("SELECT * FROM INVITES WHERE server=? AND von=?", tuple([ctx.guild.id, str(ctx.message.author)]))

        invites = len(self.cur_main.fetchall())
        embed = discord.Embed(title="Invites", description=f"Du hast bereits erfolgreich {invites} Personen eingeladen.", color=0x1acdee)
        embed.set_author(name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

        if args:
            return invites
        else:
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(info(bot))