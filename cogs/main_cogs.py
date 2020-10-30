from discord.ext import commands
import discord
import time
import asyncio
from math import ceil
import random
import string


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

        with open("trashtalk.txt", encoding="utf-8") as file:
            self.text = file.readlines()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot {} läuft!".format(self.bot.user))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(ctx.guild.channels, name="angeliwiese")
        if channel is not None:
            await channel.send('Selam {}, willkommen in der Familie!\nHast du Ärger, gehst du Cafe Al Bustan, gehst du zu Arafat!'.format(member))

    @commands.command()
    async def trashtalk(self, ctx, *args):
        users_to_tt = [ctx.message.guild.get_member(int(str(x).strip("<>!@"))) for x in args]

        for user in users_to_tt:
            for t in self.text:
                await user.send(t)

    @commands.command()
    async def amo(self, ctx, *args):
        y = [mem for mem in [m for m in ctx.guild.members if m != ctx.message.author] if
             "AMO" in [x.name for x in mem.roles]]

        for x in y:
            await x.send("{}".format(" ".join(args)))

    @commands.command()
    async def mafia(self, ctx, *args):
        guild = ctx.message.guild
        users_to_play = [guild.get_member(int(str(x).strip("<>!@"))) for x in args]
        roles_before_game = {}

        if ctx.message.author not in users_to_play:
            users_to_play.append(ctx.message.author)

        accepted_user = []

        bot_sent_messages = []

        for x in users_to_play:
            request = await x.send(f"Du wurdest von {ctx.message.author} eingeladen Mafia zu spielen. Möchtest du mitspielen?")
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
                bot_sent_messages.append(await x.send('Du warst leider zu langsam'))
                
            else:
                if reaction.emoji == '👍':
                    invite = True
                    bot_sent_messages.append(await x.send("Einladung erfolgreich angenommen!"))

                if reaction.emoji == '👎':
                    bot_sent_messages.append(await x.send("Einladung erfolgreich abgelehnt!"))

            if invite:
                accepted_user.append(x)

        for x in bot_sent_messages:
            await x.delete()

        game_id = ''.join(random.choice(string.ascii_letters) for x in range(6)).upper()
        await ctx.send(f"Spiel: {game_id} wird gestartet.")

        # Eigentlichen Rollen entfernen
        not_allowed = [481248489238429727, 710895965761962104]

        for x in users_to_play:
            real_role = []

            for f in x.roles:
                if f.id not in not_allowed:
                    real_role.append(f)

            roles_before_game[x] = real_role

            await x.remove_roles(*real_role)

        if len(accepted_user) < 3:
            await ctx.send(f"Spiel: {game_id} konnte nicht gestartet werden, da zu wenige Spieler vorhanden sind.")
            return

        game_id = ''.join(random.choice(string.ascii_letters) for x in range(6)).upper()

        mafia_count = ceil(len(accepted_user) / 5)
        mafias = []
        to_select = accepted_user.copy()

        for x in range(mafia_count):
            f = random.choice(to_select)
            mafias.append(f)
            to_select.remove(f)

        print("Not Mafia: ", to_select)
        print("Mafias: ", mafias)

        mafia_role = await guild.create_role(name=''.join(random.choice(string.ascii_letters) for x in range(8)).upper())

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            mafia_role: discord.PermissionOverwrite(read_messages=True)
        }

        mafia_channel = await guild.create_text_channel(f'mafia {game_id}', overwrites=overwrites)

        for x in mafias:
            await x.add_roles(mafia_role)

        for count, x in enumerate(range(len(to_select))):

            pp_role = await guild.create_role(name=''.join(random.choice(string.ascii_letters) for x in range(8)).upper())

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                pp_role: discord.PermissionOverwrite(read_messages=True)
            }

            await guild.create_text_channel(f'person{count + 1} {game_id}', overwrites=overwrites)

            user = random.choice(to_select)
            await user.add_roles(pp_role)
            to_select.remove(user)

        await ctx.send("Spiel erfolgreich gestartet.")
        await ctx.send("Ihr habt nun 5 Minuten Zeit bis zur ersten Abstimmung! " + ' '.join([x.mention for x in accepted_user]))




        await ctx.send("Spiel beendet")

        for x in users_to_play:
            await x.add_roles(*old_roles[x])

    @commands.command()
    async def ar(self, ctx, *args):
        old_roles = {}

        users_to_play = [ctx.message.guild.get_member(int(str(x).strip("<>!@"))) for x in args]
        not_allowed = [481248489238429727, 710895965761962104]

        for x in users_to_play:
            real_role = []

            for f in x.roles:
                if f.id not in not_allowed:
                    real_role.append(f)


            old_roles[x] = real_role

            await x.remove_roles(*real_role)
            await ctx.send("Gelöscht, 10 Sekunden warten und dann Back nigga")
            time.sleep(10)

        for x in users_to_play:
            await x.add_roles(*old_roles[x])

    @commands.command()
    async def delete_unwanted(self, ctx, *args):
        not_allowed = [481248489238429727, 710895965761962104, 768176239495610398, 768172546860253194, 770040428496945173, 768172546104229899, 768176269916635176, 770331799246995508]

        for x in ctx.guild.roles:
            if x.id not in not_allowed:
                await x.delete()

        await ctx.send("Ungewolte Rollen wurden Gelöscht.")

    @commands.command()
    async def show_roles(self, ctx, *args):
        print([x for x in ctx.guild.roles])

    @commands.command()
    async def channel_id(self, ctx, *args):
        channel = discord.utils.get(ctx.guild.channels, name="angeliwiese")
        print(channel.id)

def setup(bot):
    bot.add_cog(Basic(bot))
