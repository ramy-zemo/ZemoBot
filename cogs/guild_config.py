import re

from discord import Role, Embed
from discord.ext import commands


class GuildConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def set_auto_role(self, ctx, role: Role):
        self.bot.ApiClient.request(self.bot.ApiClient.change_auto_role,
                                   params={"guild_id": ctx.guild.id, "role_id": role.id})

        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        title = self.bot.language(self.bot, lang, "WELCOME_ROLE_CHANGED_TITLE")
        description = self.bot.language(self.bot, lang, "WELCOME_ROLE_CHANGED_DESCRIPTION", server=ctx.guild, role=role)

        embed = Embed(color=0x1acdee, title=title, description=description)
        embed.set_author(name="Zemo Bot")
        embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def set_prefix(self, ctx, prefix):
        self.bot.ApiClient.request(self.bot.ApiClient.change_prefix,
                                   params={"guild_id": ctx.guild.id, "prefix": prefix})

        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        title = self.bot.language(self.bot, lang, "PREFIX_CHANGED_TITLE")
        description = self.bot.language(self.bot, lang, "PREFIX_CHANGED_DESCRIPTION", server=ctx.guild, prefix=prefix)

        embed = Embed(color=0x1acdee, title=title, description=description)
        embed.set_author(name="Zemo Bot")
        embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def enable_command(self, ctx, command):
        all_guild_commands = self.bot.ApiClient.request(self.bot.ApiClient.get_all_guild_commands_and_category,
                                                        params={"guild_id": ctx.guild.id})

        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        if command in all_guild_commands:
            title = self.bot.language(self.bot, lang, "COMMAND_ENABLED_TITLE")
            description = self.bot.language(self.bot, lang, "COMMAND_ENABLED_DESCRIPTION",
                                            server=ctx.guild, command=command)

            self.bot.ApiClient.request(self.bot.ApiClient.enable_command,
                                       params={"guild_id": ctx.guild.id, "command": command})

            embed = Embed(color=0x1acdee, title=title, description=description)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)

        else:
            title = self.bot.language(self.bot, lang, "COMMAND_NOT_FOUND_TITLE")
            description = self.bot.language(self.bot, lang, "COMMAND_NOT_FOUND_DESCRIPTION")
            embed = Embed(color=0x1acdee, title=title, description=description)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def disable_command(self, ctx, command):
        all_guild_commands = self.bot.ApiClient.request(self.bot.ApiClient.get_all_guild_commands_and_category,
                                                        params={"guild_id": ctx.guild.id})

        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        if command in all_guild_commands:
            title = self.bot.language(self.bot, lang, "COMMAND_DISABLED_TITLE")
            description = self.bot.language(self.bot, lang, "COMMAND_DISABLED_DESCRIPTION")

            self.bot.ApiClient.request(self.bot.ApiClient.disable_command,
                                       params={"guild_id": ctx.guild.id, "command": command})
            embed = Embed(color=0x1acdee, title=title, description=description)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)

        else:
            title = self.bot.language(self.bot, lang, "COMMAND_NOT_FOUND_TITLE")
            description = self.bot.language(self.bot, lang, "COMMAND_NOT_FOUND_DESCRIPTION")

            embed = Embed(color=0x1acdee, title=title, description=description)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def change_welcome_message(self, ctx, *args):
        message = ' '.join(args)
        parameters_in_string = re.findall("(?<={)(.*)(?=})", message)
        available_parameters = ["member", "inviter"]

        lang = self.bot.guild_languages.get(ctx.guild.id, "en")

        if all([True if param in available_parameters else False for param in parameters_in_string]):
            self.bot.ApiClient.request(self.bot.ApiClient.change_welcome_message,
                                       params={"guild_id": ctx.guild.id, "welcome_msg": message})

            title = self.bot.language(self.bot, lang, "WELCOME_MESSAGE_CHANGED_TITLE")
            description = self.bot.language(self.bot, lang, "WELCOME_MESSAGE_CHANGED_DESCRIPTION")

            embed = Embed(color=0x00ff00, title=title, description=description)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)

        else:
            title = self.bot.language(self.bot, lang, "WELCOME_MESSAGE_CHANGED_ERROR_TITLE")
            description = self.bot.language(self.bot, lang, "WELCOME_MESSAGE_CHANGED_ERROR_DESCRIPTION")

            embed = Embed(color=0xff0000, title=title, description=description)
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GuildConfig(bot))
