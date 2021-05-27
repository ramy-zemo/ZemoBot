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

        embed = Embed(color=0x1acdee,
                      description=f"Die Willkommensrolle für {ctx.guild} wurde erfolgreich zu {role} geändert.")
        embed.set_author(name="Zemo Bot")
        embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def set_prefix(self, ctx, prefix):
        self.bot.ApiClient.request(self.bot.ApiClient.change_prefix,
                                   params={"guild_id": ctx.guild.id, "prefix": prefix})

        embed = Embed(color=0x1acdee,
                      description=f"Der Befehlsprefix für {ctx.guild} wurde erfolgreich zu {prefix} geändert.")
        embed.set_author(name="Zemo Bot")
        embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def enable_command(self, ctx, command):
        all_guild_commands = self.bot.ApiClient.request(self.bot.ApiClient.get_all_guild_commands_and_category,
                                                        params={"guild_id": ctx.guild.id})

        if command in all_guild_commands:
            self.bot.ApiClient.request(self.bot.ApiClient.enable_command,
                                       params={"guild_id": ctx.guild.id, "command": command})
            embed = Embed(color=0x1acdee,
                          description=f"Command {command} erfolgreich für den Server {ctx.guild} aktiviert.")
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)

        else:
            embed = Embed(color=0x1acdee,
                          description="Command nicht gefunden. Bitte gib den Command ohne Prefix ein.")
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def disable_command(self, ctx, command):
        all_guild_commands = self.bot.ApiClient.request(self.bot.ApiClient.get_all_guild_commands_and_category,
                                                        params={"guild_id": ctx.guild.id})

        if command in all_guild_commands:
            self.bot.ApiClient.request(self.bot.ApiClient.disable_command,
                                       params={"guild_id": ctx.guild.id, "command": command})
            embed = Embed(color=0x1acdee,
                          description=f"Command {command} erfolgreich für den Server {ctx.guild} deaktiviert.")
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)

        else:
            embed = Embed(color=0x1acdee,
                          description="Command nicht gefunden. Bitte gib den Command ohne Prefix ein.")
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def change_welcome_message(self, ctx, *args):
        message = ' '.join(args)
        parameters_in_string = re.findall("(?<={)(.*)(?=})", message)
        available_parameters = ["member", "inviter"]

        if all([True if param in available_parameters else False for param in parameters_in_string]):
            self.bot.ApiClient.request(self.bot.ApiClient.change_welcome_message,
                                       params={"guild_id": ctx.guild.id, "welcome_msg": message})
            embed = Embed(color=0x00ff00,
                          description="Willkommensnachricht erfolgreich geändert.")
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)
        else:
            embed = Embed(color=0xff0000,
                          description="Falsche Parameter übergeben. Mögliche Parameter:\n {member} {inviter}")
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GuildConfig(bot))
