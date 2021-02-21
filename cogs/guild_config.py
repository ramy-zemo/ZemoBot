from discord import Role, Embed
from discord.ext import commands
from etc.sql_reference import change_auto_role, change_prefix, disable_command, enable_command, set_welcome_message
import re


class GuildConfig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def set_auto_role(self, ctx, role: Role):
        change_auto_role(ctx.guild.id, role.id)
        embed = Embed(color=0x1acdee, description=f"Die Willkommensrolle für {ctx.guild} wurde erfolgreich zu {role} geändert.")
        embed.set_author(name="Zemo Bot")
        embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def set_prefix(self, ctx, prefix):
        change_prefix(ctx.guild.id, prefix)
        embed = Embed(color=0x1acdee, description=f"Der Befehlsprefix für {ctx.guild} wurde erfolgreich zu {prefix} geändert.")
        embed.set_author(name="Zemo Bot")
        embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command()
    async def enable_command(self, ctx, command):
        if command in self.bot.user_commands:
            enable_command(ctx.guild.id, command)
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
        if command in self.bot.user_commands:
            disable_command(ctx.guild.id, command)
            enable_command(ctx.guild.id, command)
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
    async def set_welcome_message(self, ctx, *args):
        message = ' '.join(args)
        parameters_in_string = re.findall("(?<={)(.*)(?=})", message)
        available_parameters = ["member", "inviter"]

        if all([True if param in available_parameters else False for param in parameters_in_string]):
            set_welcome_message(ctx.guild.id, message)
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
