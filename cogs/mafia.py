import discord
import asyncio

from discord.ext import commands
from string import ascii_letters
from random import choice
from math import ceil


class Mafia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mafia(self, ctx, *args):
        guild = ctx.message.guild
        users_to_play = [guild.get_member(int(str(x).strip("<>!@"))) for x in args]
        non_removable_roles = [discord.utils.get(ctx.message.guild.roles, name="Server Booster"),
                                    discord.utils.get(ctx.message.guild.roles, name="@everyone")]

        roles_before_game = {}
        channels_before_game = {}
        bot_created_channels = []
        bot_created_roles = []
        bot_sent_messages = []
        new_roles = {}
        accepted_user = []

        # Add game starting Person to Player
        if ctx.message.author not in users_to_play:
            accepted_user.append(ctx.message.author)

        # Invite Users
        for member in users_to_play:
            embed = discord.Embed(title="Einladung:",
                                  description=f"Du wurdest von {ctx.message.author.mention} eingeladen Mafia zu spielen. Möchtest du mitspielen?",
                                  color=0x1acdee)

            embed.set_author(name="Zemo Bot",
                             icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            embed.set_footer(text="Reagiere auf diese Nachricht um die Einladung annzunehmen.")
            request = await member.send(embed=embed)

            bot_sent_messages.append(request)

            for emoji in ('👍', '👎'):
                await request.add_reaction(emoji)

            invite = False

            for emoji in ('👍', '👎'):
                await request.add_reaction(emoji)

            def check(reaction, user):
                return str(reaction.emoji) in ['👍', '👎']

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)

            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout",
                                      description="Du warst leider zu langsam!",
                                      color=0x1acdee)
                embed.set_author(name="Zemo Bot",
                                 icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
                bot_sent_messages.append(await member.send(embed=embed))

            else:
                if reaction.emoji == '👍':
                    invite = True
                    embed = discord.Embed(title="Einladung",
                                          description="Einladung erfolgreich angenommen.\n"
                                                      "Das Spiel startet in kürze.",
                                          color=0x00f030)

                    embed.set_author(name="Zemo Bot",
                                     icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
                    bot_sent_messages.append(await member.send(embed=embed))

                if reaction.emoji == '👎':
                    embed = discord.Embed(title="Einladung",
                                          description="Einladung erfolgreich abgelehnt!\n",
                                          color=0xf00000)

                    embed.set_author(name="Zemo Bot",
                                     icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
                    bot_sent_messages.append(await member.send(embed=embed))

            if invite:
                accepted_user.append(member)

        # Define Game ID
        game_id = ''.join(choice(ascii_letters) for x in range(6)).upper()

        # End Game, not enough Users
        if len(accepted_user) < 3:
            embed = discord.Embed(title="Spiel konnte nicht gestartet werden",
                                  description=f"Spiel: {game_id} konnte nicht gestartet werden, da zu wenige Spieler vorhanden sind.",
                                  color=0xf00000)

            embed.set_author(name="Zemo Bot",
                             icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

            return bot_sent_messages.append(await ctx.send(embed=embed))

        # Send Game Start Notification
        await ctx.send(f"Spiel: {game_id} wird gestartet.")

        # Save old Voice Channels
        for x in accepted_user:
            channels_before_game[x] = x.voice.channel

        # Delete old Roles and save them
        for x in accepted_user:
            real_role = []

            for f in x.roles:
                if f not in non_removable_roles:
                    real_role.append(f)

            roles_before_game[x] = real_role
            print(*real_role)
            await x.remove_roles(*real_role)

        mafia_count = ceil(len(accepted_user) / 5)
        mafias = []
        to_select = accepted_user.copy()

        for x in range(mafia_count):
            f = choice(to_select)
            mafias.append(f)
            to_select.remove(f)

        vote_persons = to_select.copy()
        vote_mafias = mafias.copy()

        # Create Game Channels and Roles
        game_category = await ctx.guild.create_category(f"MafiaGame {game_id}")
        bot_created_channels.append(game_category)

        overwrites_voice = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }
        game_voice = await ctx.guild.create_voice_channel(f"MafiaGame {game_id}", category=game_category,
                                                          overwrites=overwrites_voice)

        bot_created_channels.append(game_voice)

        for count, x in enumerate(range(len(to_select))):
            pp_role = await guild.create_role(
                name=''.join(choice(ascii_letters) for x in range(8)).upper())
            bot_created_roles.append(pp_role)

            overwrites_person = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                pp_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True)
            }

            bot_created_channels.append(
                await guild.create_text_channel(f'person {game_id}', overwrites=overwrites_person,
                                                category=game_category))

            new_roles[x] = pp_role
            user = choice(to_select)
            await user.add_roles(pp_role)
            to_select.remove(user)

        mafia_role = await guild.create_role(
            name=''.join(choice(ascii_letters) for x in range(8)).upper())

        bot_created_roles.append(mafia_role)

        overwrites_mafia_channel = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            mafia_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True)
        }

        mafia_channel = await guild.create_text_channel(f'mafia {game_id}', overwrites=overwrites_mafia_channel,
                                                        category=game_category)
        bot_created_channels.append(mafia_channel)

        overwrites_text = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }

        for rl in bot_created_roles:
            overwrites_text[rl] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        game_text_channel = await guild.create_text_channel(f'Gamechat', category=game_category,
                                                            overwrites=overwrites_text)
        bot_created_channels.append(game_text_channel)

        for mafia in mafias:
            await mafia.add_roles(mafia_role)
            new_roles[mafia] = mafia_role

        # Change Category Permissions
        overwrites_category = {
            ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }

        for role in bot_created_roles:
            overwrites_category[role] = discord.PermissionOverwrite(read_messages=True, use_voice_activation=True)

        await game_category.edit(sync_permissions=False, overwrites=overwrites_category)

        # Change Voice Permissions
        overwrites_voice = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }

        for role in bot_created_roles:
            overwrites_voice[role] = discord.PermissionOverwrite(speak=True, use_voice_activation=True, read_messages=True, )

        await game_voice.edit(sync_permissions=False, overwrites=overwrites_voice)

        # Move players to Voice Channel
        while True:
            try:
                for user in accepted_user:
                    await user.edit(voice_channel=game_voice)
                break
            except discord.errors.HTTPException:
                await ctx.send("Alle mitspieler müssen mit einem Sprachkanal verbunden sein.\n"
                                             "Versuche in 15 Sekunden erneut.")
                await asyncio.sleep(15)

        # Notify users
        for user in vote_mafias:
            bot_sent_messages.append(await user.send("Gratuliere, du bist ein Mafia mitglied."))

        for user in vote_persons:
            bot_sent_messages.append(await user.send("Gratuliere, du bist ein normaler Bürger."))

        # Start Game
        embed = discord.Embed(title="Spiel erfolgreich gestartet.",
                              description="Ihr habt nun 5 Minuten Zeit bis zur ersten Abstimmung.\nViel Glück!\n\n",
                              color=0x1acdee)

        embed.set_author(name="Zemo Bot",
                         icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

        embed.add_field(name="Mitspieler:", value="\n" + ' '.join([x.mention for x in accepted_user]), inline=True)

        await game_text_channel.send(embed=embed)

        # Game Body
        users_to_play = accepted_user.copy()

        while True:
            # Check if Game is still running
            if len(vote_mafias) < len(vote_persons) and len(vote_mafias) != 0:
                await asyncio.sleep(30)
                votes = []
                # Get all User Votes
                for user in users_to_play:
                    await game_text_channel.send(f"{user.mention} für wen stimmst du?")

                    def check_vote(m):
                        try:
                            user_input = guild.get_member(int(str(m.content).strip("<>!@")))
                            # Right Person is voting
                            first_check = m.author == user

                            # Voted Person is still "alive"
                            second_check = user_input in users_to_play

                            # Check the channel
                            third_check = m.channel == game_text_channel
                            # Skip vote
                            return first_check and second_check and third_check
                        except:
                            if m.content.lower() == "skip":
                                return True
                            else:
                                return False

                    answer = await self.bot.wait_for("message", check=check_vote)
                    votes.append(answer.content)

                raus = []

                for vote in votes:
                    if votes.count(vote) > len(votes) / 2:
                        raus.append(vote)

                # Check if someone gets kicked
                if raus == [] or "skip" in raus:
                    # Dont kick
                    await game_text_channel.send("Es konnte keine mehrheit gebildet werden.")
                    await game_text_channel.send("5 Minuten bis zur nächsten Abstimmung.")

                else:
                    # Kick Person and notify Users
                    to_kick = guild.get_member(int(str(raus[0]).strip("<>!@")))
                    users_to_play.remove(to_kick)

                    await game_text_channel.send(f"{raus[0]} wird raus geworfen")

                    if to_kick in vote_mafias:
                        vote_mafias.remove(to_kick)
                        await game_text_channel.send(f"{raus[0]} war ein Mafioso")
                    elif to_kick in vote_persons:
                        vote_persons.remove(to_kick)
                        await game_text_channel.send(f"{raus[0]} war ein Bürger")

                    await to_kick.edit(mute=True)

                    if len(vote_mafias) != 0 and len(vote_mafias) < len(vote_persons):
                        await game_text_channel.send("5 Minuten bis zur nächsten Abstimmung.")

            else:
                # Game is not running
                if len(vote_mafias) >= len(vote_persons):
                    await game_text_channel.send("Die Mafiosi haben gewonnen")

                else:
                    await game_text_channel.send(f"Die Bürger haben gewonnen.")

                # Add old roles & unmute Users & move Players back to old Voice Channel
                for x in accepted_user:
                    await x.add_roles(*roles_before_game[x])
                    await x.edit(mute=False)
                    await x.edit(voice_channel=channels_before_game[x])

                await asyncio.sleep(60)

                # Delete all Bot sent messages
                for msg in bot_sent_messages:
                    await msg.delete()

                await ctx.send(f"Spiel {game_id} beendet")
                break


def setup(bot):
    bot.add_cog(Mafia(bot))
