from discord.ext import commands
import sqlite3
import discord
import requests
import time

class to_much_reaction(Exception):
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

        async def ask(question, options, max_count):
            sent_messages = []
            while True:
                embed = discord.Embed(title=question, description='\n'.join(options), color=0x1acdee)

                embed.set_author(name="Zemo Bot",
                                 icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
                embed.set_footer(text=f"Reagiere auf diese Nachricht um eine Auswahl zu treffen. Maximale Auswahlmöglichkeiten: {max_count}")

                request = await text_channel.send(embed=embed)
                sent_messages.append(request)
                emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

                for count in range(len(options)):
                    await request.add_reaction(emojis[count])
                else:
                    await request.add_reaction("⏭")

                self.reactions = []

                def check(reaction, user):
                    if str(user) == str(self.bot.user):
                        return False
                    if reaction.emoji != "⏭":
                        self.reactions.append(reaction)

                    if str(reaction.emoji) in ["⏭"]:
                        if len(self.reactions) > max_count:
                            raise to_much_reaction
                        return True

                try:
                    reaction, usr = await self.bot.wait_for('reaction_add', check=check)

                except to_much_reaction:
                    embed = discord.Embed(title="Zu viele Optionen gewählt", description=f"Du hast zu viele Optionen gewählt. Wähle maximal {max_count}", color=0x1acdee)

                    embed.set_author(name="Zemo Bot",icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
                    embed.set_footer(text=f"Reagiere auf die nächste Nachricht um eine Auswahl zu treffen. Maximale Auswahlmöglichkeiten: {max_count}")
                    sent_messages.append(await text_channel.send(embed=embed))
                    continue

                # Delete sent messages
                for msg in sent_messages:
                    await msg.delete()
                await text_channel.send("Vielen Dank für die Antwort.")
                return self.reactions

        welcome_message = await text_channel.send(f"Willkommen {user.mention}")

        category_option = await ask("Was suchst du?", ["1. Gaming", "2. Dating", "3. Friends"], 1)
        print("Ende: ", category_option)

def setup(bot):
    bot.add_cog(partner(bot))