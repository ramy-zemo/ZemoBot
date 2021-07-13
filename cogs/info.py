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
        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        if not member:
            user = ctx.message.author
        else:
            user = member

        messages = self.bot.ApiClient.request(self.bot.ApiClient.get_user_messages, params={"user_id": user.id})
        minutes = self.bot.ApiClient.request(self.bot.ApiClient.get_user_voice_time, params={"user_id": user.id})
        trashtalk = self.bot.ApiClient.request(self.bot.ApiClient.get_user_trashtalk,
                                               params={"guild_id": ctx.guild.id, "user_id": user.id})

        title = self.bot.language(self.bot, lang, "INFO_TITLE")
        description = self.bot.language(self.bot, lang, "INFO_DESCRIPTION")

        fields_messages = self.bot.language(self.bot, lang, "INFO_FIELDS_MESSAGES")
        fields_messages_value = self.bot.language(self.bot, lang, "INFO_FIELDS_MESSAGES_VALUE",
                                                  message_count=len(messages))

        fields_invites = self.bot.language(self.bot, lang, "INFO_FIELDS_INVITES")
        fields_invites_value = self.bot.language(self.bot, lang, "INFO_FIELDS_INVITES_VALUE",
                                                 invite_count=len(await self.invites(ctx, user, "No Print")))

        fields_voice_time = self.bot.language(self.bot, lang, "INFO_FIELDS_VOICE_TIME")
        fields_voice_time_value = self.bot.language(self.bot, lang, "INFO_FIELDS_VOICE_TIME_VALUE", voice_time=minutes)

        fields_trashtalk = self.bot.language(self.bot, lang, "INFO_FIELDS_TRASHTALK")
        fields_trashtalk_value = self.bot.language(self.bot, lang, "INFO_FIELDS_TRASHTALK_VALUE",
                                                   trashtalk_count=len(trashtalk))

        embed = discord.Embed(title=title, description=description, color=0x1acdee)
        embed.add_field(name=fields_messages, value=fields_messages_value, inline=False)
        embed.add_field(name=fields_invites, value=fields_invites_value, inline=False)
        embed.add_field(name=fields_voice_time, value=fields_voice_time_value, inline=False)
        embed.add_field(name=fields_trashtalk, value=fields_trashtalk_value, inline=False)

        embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx, category: str = None):
        prefix = self.bot.ApiClient.request(self.bot.ApiClient.get_prefix, params={"guild_id": ctx.guild.id})
        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

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
            print(command_list)
            command_dict = {command + " " + parameter if parameter else command: description
                            for command, parameter, description in command_list}

            embed = discord.Embed(color=0x1acdee)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

            for command in command_dict:
                if command not in disabled_commands:
                    embed.add_field(name=prefix + command,
                                    value=self.bot.language(self.bot, lang, f"{command.split()[0].upper()}_COMMAND"),
                                    inline=False)

            await ctx.send(embed=embed)

        else:
            return await invalid_argument(self, ctx, "help")

    @commands.command()
    async def invites(self, ctx, member=None, *args):
        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

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
            title = self.bot.language(self.bot, lang, "INFO_FIELDS_INVITES")
            description = self.bot.language(self.bot, lang, "INFO_FIELDS_INVITES_VALUE", invite_count=invites)

            embed = discord.Embed(title=title, description=description, color=0x1acdee)
            embed.set_author(name="Zemo Bot", icon_url=self.bot.icon_url)
            await ctx.send(embed=embed)

    @commands.command()
    async def server_info(self, ctx):
        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        title = self.bot.language(self.bot, lang, "SERVER_INFO_TITLE")
        description = self.bot.language(self.bot, lang, "SERVER_INFO_DESCRIPTION")
        cpu = self.bot.language(self.bot, lang, "SERVER_INFO_CPU_NAME")
        ram = self.bot.language(self.bot, lang, "SERVER_INFO_RAM_NAME")
        processes = self.bot.language(self.bot, lang, "SERVER_INFO_PROCESS_NAME")
        boot_time = self.bot.language(self.bot, lang, "SERVER_INFO_BOOT_TIME_NAME")

        embed = discord.Embed(title=title, description=description, color=0x1acdee)

        embed.add_field(name=cpu, value=psutil.cpu_percent(interval=1), inline=False)
        embed.add_field(name=ram, value=round(psutil.virtual_memory()[0] / 1000000000, 2), inline=False)
        embed.add_field(name=processes, value=str(len(psutil.pids())), inline=False)
        embed.add_field(name=boot_time,
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
