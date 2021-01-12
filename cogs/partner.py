from discord.ext import commands
import discord
from ZemoBot.etc.ask import ask


class Partner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_in_partner = []

    @commands.command()
    async def partner(self, ctx):
        user = ctx.message.author
        guild = ctx.guild

        if user in self.current_in_partner:
            return 1

        self.current_in_partner.append(user)

        text_role = await guild.create_role(name=f"partner {user}")

        overwrites_text = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, read_message_history=False,
                                                            send_messages=False),
            text_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True)
        }

        text_channel = await guild.create_text_channel(f"partner {user}", overwrites=overwrites_text)

        await user.add_roles(text_role)

        welcome_message = await text_channel.send(f"Willkommen {user.mention}")

        category_option = await ask(ctx.message.author, "reaction_add", "Was suchst du?", text_channel, self.bot,
                                    ["1. Gaming", "2. Dating", "3. Friends"], 1, )

        age_option = await ask(ctx.message.author, "message", "Wie alt bist du?", text_channel, self.bot, range_int=[14, 70],
                               msg_type="int", max_answers=1)
        print(age_option)
        print(category_option)


def setup(bot):
    bot.add_cog(Partner(bot))
