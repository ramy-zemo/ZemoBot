from discord.ext import commands
import sqlite3
import discord


class ToMuchReaction(Exception):
    pass


class InvalidInt(Exception):
    pass


class partner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()
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
           guild.default_role: discord.PermissionOverwrite(read_messages=False, read_message_history=False, send_messages=False),
           text_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=True)
        }

        text_channel = await guild.create_text_channel(f"partner {user}", overwrites=overwrites_text)

        await user.add_roles(text_role)

        async def ask(type, question, options=[], max_answers=9999, range_int=[0, 100], msg_type="text"):
            sent_messages = []
            while True:
                embed = discord.Embed(title=question, description='\n'.join(options), color=0x1acdee)

                embed.set_author(name="Zemo Bot",
                                 icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
                embed.set_footer(text=f"Reagiere auf diese Nachricht um eine Auswahl zu treffen. Maximale Auswahlmöglichkeiten: {max_answers}")

                request = await text_channel.send(embed=embed)
                sent_messages.append(request)
                emojis = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"}

                if type == "reaction_add":
                    for count in range(len(options)):
                        await request.add_reaction(emojis[count + 1])
                    else:
                        await request.add_reaction("⏭")

                self.reactions = []

                req = await text_channel.fetch_message(request.id)

                def reaction_add(reaction, user):
                    return print(reaction, user)
                    print(req.reactions)
                    if reaction.message.channel != text_channel:
                        return
                    if str(user) == str(self.bot.user):
                        return False
                    if reaction.emoji != "⏭":
                        self.reactions.append(reaction)

                    if str(reaction.emoji) in ["⏭"]:
                        print(req.reactions)
                        if len(req.reactions) > max_answers:
                            raise ToMuchReaction
                        return True

                def check_message(reaction):
                    if reaction.channel != text_channel or str(reaction.author) == str(self.bot.user):
                        return

                    if msg_type == "int":
                        if range_int != [0, 100]:
                            try:
                                if range_int[0] < int(reaction.content) < range_int[1]:
                                    return True
                                elif int(reaction.content) < range_int[0]:
                                    raise InvalidInt
                                elif int(reaction.content) > range_int[1]:
                                    raise InvalidInt

                            except ValueError:
                                raise InvalidInt
                        else:
                            try:
                                int(reaction.content)
                            except ValueError:
                                raise InvalidInt
                    else:
                        return True

                try:
                    check_methods = {"reaction_add": reaction_add, "message": check_message}
                    reaction = await self.bot.wait_for(type, check=check_methods[type])

                except ToMuchReaction:
                    embed = discord.Embed(title="Zu viele Optionen gewählt", description=f"Du hast zu viele Optionen gewählt. Wähle maximal {max_answers}", color=0x1acdee)
                    embed.set_author(name="Zemo Bot",icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
                    embed.set_footer(text=f"Reagiere auf die nächste Nachricht um eine Auswahl zu treffen. Maximale Auswahlmöglichkeiten: {max_answers}")
                    sent_messages.append(await text_channel.send(embed=embed))
                    continue

                except InvalidInt:
                    embed = discord.Embed(title="Ungültige Auswahl", description=f"Die eingegebene Zahl ist nicht gültig.", color=0x1acdee)
                    embed.set_author(name="Zemo Bot",icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
                    embed.set_footer(text=f"Die Auswahl muss zwischen {range_int[0]} und {range_int[1]} liegen.")
                    sent_messages.append(await text_channel.send(embed=embed))
                    continue

                # Delete sent messages
                for msg in sent_messages:
                    await msg.delete()
                await text_channel.send("Vielen Dank für die Antwort.")

                answers = []

                if type == "reaction_add":
                    for answer in [x.emoji for x in self.reactions]:
                        for count, emoji in enumerate(emojis):
                            if answer == emojis[emoji]:
                                answers.append(count + 1)

                elif type == "message":
                    return reaction.content

                return answers

        welcome_message = await text_channel.send(f"Willkommen {user.mention}")

        category_option = await ask("reaction_add", "Was suchst du?", ["1. Gaming", "2. Dating", "3. Friends"], 1)
        age_option = await ask("message", "Wie alt bist du?", range_int=[14, 70], msg_type="int", max_answers=1)
        print(age_option)
        print(category_option)


def setup(bot):
    bot.add_cog(partner(bot))
