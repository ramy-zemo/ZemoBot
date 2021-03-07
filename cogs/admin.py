from discord.ext import commands
# from discord_local.ext.commands.bot import process_commands
from sql.commands import create_command, delete_command
from sql.admin_commands import create_admin_command, delete_admin_command


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_command(self, ctx, category, command, parameters, description):
        create_command(category, command, parameters, description)

    @commands.command()
    async def add_admin_command(self, ctx, command, parameters, description):
        create_admin_command(command, parameters, description)

    @commands.command()
    async def delete_command(self, ctx, command):
        delete_command(command)

    @commands.command()
    async def delete_admin_command(self, ctx, command):
        delete_admin_command(command)


def setup(bot):
    bot.add_cog(Admin(bot))
