from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_command(self, ctx, category, command, parameters, description):
        self.bot.ApiClient.request(self.bot.ApiClient.create_command,
                                   params={"category": category,
                                           "command": command,
                                           "parameters": parameters,
                                           "description": description})

    @commands.command()
    async def add_admin_command(self, ctx, command, parameters, description):
        self.bot.ApiClient.request(self.bot.ApiClient.create_admin_command,
                                   params={"command": command,
                                           "parameters": parameters,
                                           "description": description})

    @commands.command()
    async def delete_command(self, ctx, command):
        self.bot.ApiClient.request(self.bot.ApiClient.delete_command, params={"command": command})

    @commands.command()
    async def delete_admin_command(self, ctx, command):
        self.bot.ApiClient.request(self.bot.ApiClient.delete_admin_command, params={"command": command})


def setup(bot):
    bot.add_cog(Admin(bot))
