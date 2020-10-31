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
        self.not_allowed = [481248489238429727, 710895965761962104]
        self.allowed_roles = [481248489238429727, 710895965761962104, 768176239495610398, 768172546860253194, 770040428496945173, 768172546104229899, 768176269916635176, 770331799246995508]
        self.allowed_channels = [
            768172543273730058,
            768175708799107192,
            768176881735696384,
            768177068630212648,
            768177563633713242,
            768177809801609275,
            768177845264056359,
            768177889891188757,
            768179070751735818,
            768179163919679548,
            768179253883306035,
            768179505595940874,
            768179640765906964,
            769921393281466408,
            769921666779185173,
            769921717887172608,
            769922292297367603,
            771868769983004682]

        with open("trashtalk.txt", encoding="utf-8") as file:
            self.text = file.readlines()

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot {} läuft!".format(self.bot.user))

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        channel = discord.utils.get(ctx.guild.channels, name="willkommen")

        if channel is not None:
            await channel.send('Selam {}, willkommen in der Familie!\nHast du Ärger, gehst du Cafe Al Zemo, gehst du zu Ramo!'.format(ctx.mention))

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
        new_roles = {}
        running = True

        if ctx.message.author not in users_to_play:
            users_to_play.append(ctx.message.author)

        accepted_user = []
        bot_created_channels = []
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

        for msg in bot_sent_messages:
            await msg.delete()

        game_id = ''.join(random.choice(string.ascii_letters) for x in range(6)).upper()
        await ctx.send(f"Spiel: {game_id} wird gestartet.")

        if len(accepted_user) < 3:
            await ctx.send(f"Spiel: {game_id} konnte nicht gestartet werden, da zu wenige Spieler vorhanden sind.")
            running = False

        if running:
            # Alle Rollen entfernen
            for x in users_to_play:
                real_role = []

                for f in x.roles:
                    if f.id not in self.not_allowed:
                        real_role.append(f)

                roles_before_game[x] = real_role

                await x.remove_roles(*real_role)

            mafia_count = ceil(len(accepted_user) / 5)
            mafias = []
            to_select = accepted_user.copy()

            for x in range(mafia_count):
                f = random.choice(to_select)
                mafias.append(f)
                to_select.remove(f)

            print("Not Mafia: ", to_select)
            print("Mafias: ", mafias)

            game_category = await ctx.guild.create_category(f"MafiaGame {game_id}")
            bot_created_channels.append(game_category)

            mafia_role = await guild.create_role(name=''.join(random.choice(string.ascii_letters) for x in range(8)).upper())

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                mafia_role: discord.PermissionOverwrite(read_messages=True)
            }

            mafia_channel = await guild.create_text_channel(f'mafia {game_id}', overwrites=overwrites)
            bot_created_channels.append(mafia_channel)

            for mafia in mafias:
                await mafia.add_roles(mafia_role)
                new_roles[mafia] = mafia_role

            for count, x in enumerate(range(len(to_select))):

                pp_role = await guild.create_role(name=''.join(random.choice(string.ascii_letters) for x in range(8)).upper())

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    pp_role: discord.PermissionOverwrite(read_messages=True)
                }

                bot_created_channels.append(await guild.create_text_channel(f'person{count + 1} {game_id}', overwrites=overwrites))

                new_roles[x] = pp_role
                user = random.choice(to_select)
                await user.add_roles(pp_role)
                to_select.remove(user)

            await ctx.send("Spiel erfolgreich gestartet.")
            await ctx.send("Ihr habt nun 5 Minuten Zeit bis zur ersten Abstimmung! " + ' '.join([x.mention for x in accepted_user]))

            time.sleep(30)

            for x in users_to_play:
                await x.add_roles(*roles_before_game[x])

            await self.delete_unwanted_channels(ctx, False)
            await self.delete_unwanted_roles(ctx, False)

            await ctx.send("Spiel beendet")

        else:
            print("Spiel wurde abgebrochen")

    @commands.command()
    async def ar(self, ctx, *args):
        old_roles = {}

        users_to_play = [ctx.message.guild.get_member(int(str(x).strip("<>!@"))) for x in args]

        for x in users_to_play:
            real_role = []

            for f in x.roles:
                if f.id not in self.not_allowed:
                    real_role.append(f)


            old_roles[x] = real_role

            await x.remove_roles(*real_role)
            await ctx.send("Gelöscht, 10 Sekunden warten und dann Back nigga")
            time.sleep(10)

        for x in users_to_play:
            await x.add_roles(*old_roles[x])

    @commands.command()
    async def delete_unwanted_roles(self, ctx, *args):
        for x in ctx.guild.roles:
            if x.id not in self.allowed_roles:
                await x.delete()
        if len(args) == 0:
            await ctx.send("Ungewolte Rollen wurden Gelöscht.")

    @commands.command()
    async def show_roles(self, ctx, *args):
        print([x for x in ctx.guild.roles])

    @commands.command()
    async def delete_unwanted_channels(self, ctx, *args):
        for x in ctx.guild.channels:
            if x.id not in self.allowed_channels:
                await x.delete()

        if len(args) == 0:
            await ctx.send("Ungewolte Channels wurden Gelöscht.")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")

    @commands.command()
    async def vote(self, ctx, *args):
        users_to_play = [ctx.message.guild.get_member(int(str(x).strip("<>!@"))) for x in args]
        users_to_play_mentions = args
        votes = []

        for x in range(1):
            for user in users_to_play:
                await ctx.send(f"{user.mention} für wen stimmst du?")

                def check_vote(m):
                    return (m.author == user and m.content in users_to_play_mentions and m.content != user.mention) or m.content == "skip"

                answer = await self.bot.wait_for("message", check=check_vote)
                votes.append(answer.content)

            raus = []

            for x in votes:
                if votes.count(x) > len(votes) / 2:
                    raus.append(x)

            print(raus)

            if raus == [] or "skip" in raus:
                await ctx.send("Es konnte keine mehrheit gebildet werden.")
                print(votes)

            else:
                await ctx.send(f"{raus[0]} wird raus geworfen")

def setup(bot):
    bot.add_cog(Basic(bot))
