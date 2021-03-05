import discord

from discord.ext import commands
from etc.ask import ask


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
        await text_channel.send(f"[WARNUNG] Die Partner Funktion befindet sich noch in der Beta,"
                                f" daher kann es teilweise zu Fehlfunktionen kommen. {user.mention}")

        category_option = await ask(ctx.message.author, "reaction_add", "Was suchst du?", text_channel, self.bot,
                                    ["1. Gaming", "2. Dating", "3. Friends"], 1, )

        # age_option = await ask(ctx.message.author, "message", "Wie alt bist du?", text_channel, self.bot, range_int=[14, 70], msg_type="int", max_answers=1)
        # print(age_option)

        category_option_methods = [self.gaming, self.dating, self.friends]

        await category_option_methods[category_option[0] - 1](text_channel, user, guild, text_role)

    async def gaming(self, channel, user, guild, text_role):
        available_games = ["League of Legends", "Among Us", "Apex Legends", "Fortnite",
                           "Playerunknown's Battlegrounds", "Tom Clancy's Rainbow Six Siege",
                           "Counter-Strike: Global Offensive", "Minecraft", "Call of Duty", "Grand Theft Auto"]

        available_languages = ["Chinese", "Spanish", "English", "Hindi", "Arabic", "Russian", "German", "French",
                               "Bosnian / Serbian / Croatian", "Hungarian"]

        games = await ask(user, "reaction_add", "For which game are you looking for a partner?", channel, self.bot,
                          options=[str(count + 1) + ". " + x for count, x in enumerate(available_games)])

        languages = await ask(user, "reaction_add", "What languages do you speak?", channel, self.bot,
                              options=[str(count + 1) + ". " + x for count, x in enumerate(available_languages)])

        await self.write_partner(status="initial", server=str(guild.id), user=str(user), category="gaming",
                                 games=str(games), languages=str(languages))

    async def dating(self, channel, user, guild, text_role):
        available_regions = ["Africa", "Asia", "Europe", "North America", "South America", "Australia"]
        available_interests = ["Swimming", "Cooking", "Gaming", "Sports", "Listening to music", "Playing soccer",
                               "Reading", "Programming", "Traveling", "Photographing"]

        gender = await ask(user, "reaction_add", "Please choose your gender:", channel, self.bot,
                           options=["1. Men", "2. Woman"])

        age = await ask(user, "message", "How old are you?", channel, self.bot, range_int=[14, 70], msg_type="int",
                        max_answers=1)

        region = await ask(user, "reaction_add", "Where do you live?", channel, self.bot,
                           options=[str(count + 1) + ". " + x for count, x in enumerate(available_regions)],
                           max_answers=1)

        interests = await ask(user, "reaction_add", "What are your interests?", channel, self.bot,
                              options=[str(count + 1) + ". " + x for count, x in enumerate(available_interests)])

    async def friends(self, channel, user, guild, text_role):
        print("3")

    async def write_partner(self, **kwargs):
        pass


def setup(bot):
    bot.add_cog(Partner(bot))
