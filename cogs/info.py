import datetime

import discord
import psutil

from discord.ext import commands
from etc.error_handling import invalid_argument


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx, member: discord.Member = 0):
        if not member:
            user = ctx.message.author
        else:
            user = member

        messages = self.bot.ApiClient.request(self.bot.ApiClient.get_user_messages, params={"user_id": user.id})
        minutes = self.bot.ApiClient.request(self.bot.ApiClient.get_user_voice_time, params={"user_id": user.id})
        trashtalk = self.bot.ApiClient.request(self.bot.ApiClient.get_user_trashtalk,
                                               params={"guild_id": ctx.guild.id, "user_id": user.id})

        embed = discord.Embed(title="Info", description=f"{user} Nutzerinformationen:", color=0x1acdee)
        embed.add_field(name="Nachrichten", value=f"Du hast bisher {len(messages)} Nachrichten versendet.",
                        inline=False)
        embed.add_field(name="Invites",
                        value=f"""Du hast bisher {len(await self.invites(ctx, user, "No Print"))} Invites versendet.""",
                        inline=False)
        embed.add_field(name="Minuten", value=f"Du warst {minutes} Minuten mit einem Sprachchannel verbunden.",
                        inline=False)
        embed.add_field(name="Trashtalk", value=f"""Du hast bereits {len(trashtalk)} mal Trashtalk versendet.""",
                        inline=False)
        embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, category=""):
        prefix = self.bot.ApiClient.request(self.bot.ApiClient.get_prefix, params={"guild_id": ctx.guild.id})
        disabled_commands = self.bot.ApiClient.request(self.bot.ApiClient.get_all_disabled_commands_from_guild,
                                                       params={"guild_id": ctx.guild.id})
        plugins = self.bot.ApiClient.request(self.bot.ApiClient.get_all_guild_categories,
                                             params={"guild_id": ctx.guild.id})

        if not category:
            embed = discord.Embed(color=0x1acdee)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            for plugin in plugins:
                embed.add_field(name=plugin.capitalize(), value=f"`{prefix}help {plugin}` ", inline=True)
            await ctx.send(embed=embed)

        elif category.lower() in plugins:
            command_list = self.bot.ApiClient.request(self.bot.ApiClient.get_all_guild_commands_from_category,
                                                      params={"guild_id": ctx.guild.id, "category": category})
            command_dict = {(command + " " + parameter if parameter else command): description for
                            command, parameter, description in command_list}

            embed = discord.Embed(color=0x1acdee)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

            for command in command_dict:
                if command not in disabled_commands:
                    embed.add_field(name=prefix + command, value=command_dict[command], inline=False)

            await ctx.send(embed=embed)

        else:
            return await invalid_argument(self, ctx, "help")

    @commands.command()
    async def invites(self, ctx, member="", *args):
        if member:
            invites = self.bot.ApiClient.request(self.bot.ApiClient.get_user_invites,
                                                 params={"guild_id": ctx.guild.id,
                                                         "user_id": member.id})
        else:
            invites = self.bot.ApiClient.request(self.bot.ApiClient.get_user_invites,
                                                 params={"guild_id": ctx.guild.id,
                                                         "user_id": ctx.message.author.id})

        if args:
            return invites
        else:
            embed = discord.Embed(title="Invites",
                                  description=f"Du hast bereits erfolgreich {invites} Personen eingeladen.",
                                  color=0x1acdee)
            embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def server_info(self, ctx):
        embed = discord.Embed(title="Server Infos", description="Informationen des Discord Bot Servers:",
                              color=0x1acdee)

        embed.add_field(name="CPU Percent:", value=psutil.cpu_percent(interval=1), inline=False)
        embed.add_field(name="RAM Total:", value=round(psutil.virtual_memory()[0] / 1000000000, 2), inline=False)
        embed.add_field(name="Processes running:", value=str(len(psutil.pids())), inline=False)
        embed.add_field(name="Boot Time:",
                        value=datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"),
                        inline=False)

        embed.set_author(name="Zemo Bot",
                         icon_url=self.bot.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong!  :ping_pong:  In {round(self.bot.latency * 100, 2)} ms')

    @commands.command()
    async def error(self, ctx):
        raise Exception


def setup(bot):
    bot.add_cog(Info(bot))
