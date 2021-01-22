from discord import Role, Embed
from discord.ext import commands
from etc.sql_reference import change_auto_role, change_prefix, disable_command, enable_command


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
        else:
            embed = Embed(color=0x1acdee,
                          description="Command nicht gefunden. Bitte gib den Command ohne Prefix ein.")
            embed.set_author(name="Zemo Bot")
            embed.set_thumbnail(url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GuildConfig(bot))
