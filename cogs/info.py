import datetime
import discord
import psutil
from discord.ext import commands
from etc.error_handling import invalid_argument
from etc.sql_reference import get_user_messages, get_user_voice_time, get_user_trashtalk, get_user_invites


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx, member: discord.Member = 0):
        if not member:
            user = str(ctx.message.author)
        else:
            user = member

        messages = len(get_user_messages(user))
        minutes = get_user_voice_time(user)
        trashtalk = len(get_user_trashtalk(ctx.guild.id, user))

        embed = discord.Embed(title="Info", description=f"{user} Nutzerinformationen:", color=0x1acdee)
        embed.add_field(name="Nachrichten", value=f"Du hast bisher {messages} Nachrichten versendet.", inline=False)
        embed.add_field(name="Invites",
                        value=f"""Du hast bisher {await self.invites(ctx, user, "No Print")} Invites versendet.""",
                        inline=False)
        embed.add_field(name="Minuten", value=f"Du warst {minutes} Minuten mit einem Sprachchannel verbunden.",
                        inline=False)
        embed.add_field(name="Trashtalk", value=f"""Du hast bereits {trashtalk} mal Trashtalk versendet.""",
                        inline=False)
        embed.set_author(name="Zemo Bot",
                         icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, *args):
        plugins = {
            'level': {"$trashtalk_stats": "Show your Trashtalk Stats.",
                      "$trashtalk_reset": "Reset your Trashtalk Stats.",
                      "$trashtalk_list": "Show Trashtalk Words.",
                      "$stats (member)": "Get your statistics.", "$invites": "List of your successful invites.",
                      "$info (member)": "Get your Userinformation.", "$rank": "List of Top 5 Server Ranks"},
            'fun': {"$trashtalk (*mention)": "Trashtalk people.", "$trashtalk_add": "Add Words to trashtalk.",
                    "$ping": "Check if bot is alive.",
                    "$meme": "Return random meme from Reddit.",
                    "$font (*keyword) (font)": "Returns ASCII Art, from provided Text.",
                    "$w2g (url)": "Create watch2gether room with provided Link.",
                    "$trump": "Get a random Quote of Trump.", "$trump_img": "Get a random Picture of a Trump Meme.",
                    "$gen_meme (*Top Text, Bottom Text)": "Get a custom Meme."},
            'games': {"$mafia (*mention)": "Start Mafia Game.", "$coin": "Flip a ZEMO Coin."},
            'mod': {"$auszeit (*mention) (*seconds)": "Timeout Users.", "$kick (*mention)": "Kick Members.",
                    "$ban (*mention)": "Ban Members", "$unban (*mention)": "Unban Members",
                    "$invite (max_age) (max_uses) (temporary) (unique) (reason)": "Create Invites."},
            'media': {"$font_list": "Get List of available Fonts.", "$avatar": "Get your own Discord Profile Picture.",
                      "$avatar (*mention)": "Get the Discord Avatar from another user."},
            'search': {"$faceit_finder (steam_url)": "Find a FaceIt account by Steam identifier."}
        }

        if not args:
            embed = discord.Embed(color=0x1acdee)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            embed.add_field(name="Level", value="`$help Level` ", inline=True)
            embed.add_field(name="Fun", value="`$help Fun` ", inline=True)
            embed.add_field(name="Games", value="`$help Games` ", inline=True)
            embed.add_field(name="Moderation", value="`$help Mod` ", inline=True)
            embed.add_field(name="Media", value="`$help Media` ", inline=True)
            embed.add_field(name="Search", value="`$help Search` ", inline=True)
            await ctx.send(embed=embed)

        elif len(args) == 1 and args[0].lower() in plugins:
            category = args[0].lower()
            embed = discord.Embed(color=0x1acdee)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

            for count, option in enumerate(plugins[category]):
                embed.add_field(name=option, value=plugins[category][option], inline=False)

            await ctx.send(embed=embed)

        else:
            return await invalid_argument(ctx, "help")

    @commands.command()
    async def invites(self, ctx, member="", *args):
        if args:
            return await get_user_invites(ctx.guild.id, member)
        else:
            return await get_user_invites(ctx.guild.id, ctx.message.author, ctx)

    @commands.command()
    async def server_info(self, ctx):
        embed = discord.Embed(title="Server Infos", description="Informationen des Discord Bot Servers:", color=0x1acdee)

        embed.add_field(name="CPU Percent:", value=psutil.cpu_percent(interval=1), inline=False)
        embed.add_field(name="RAM Total:", value=round(psutil.virtual_memory()[0] / 1000000000, 2), inline=False)
        embed.add_field(name="Boot Time:", value=datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        embed.add_field(name="Processes running:", value=str(len(psutil.pids())), inline=False)

        embed.set_author(name="Zemo Bot",
                         icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
