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
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(
                'Selam {}, willkommen in der Familie!\n',
                'Hast du Ärger, gehst du Cafe Al Bustan, gehst du zu Arafat!'.format(member))

    @commands.command()
    async def trashtalk(self, ctx, user: discord.User):
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
        users_to_play = [self.bot.get_user(int(str(x).strip("<>!@"))) for x in args]
        accepted_User = []

        for x in users_to_play:
            request = await x.send(f"Du wurdest von {ctx.message.author} eingeladen Mafia zu spielen. Möchtest du mitspielen?")

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
                await x.send('Du warst leider zu langsam')
                
            else:
                if reaction.emoji == '👍':
                    invite = True
                    await x.send("Einladung erfolgreich angenommen!")
                if reaction.emoji == '👎':
                    await x.send("Einladung erfolgreich abgelehnt!")

            if invite:
                accepted_User.append(x)

        game_id = ''.join(random.choice(string.ascii_letters) for x in range(6)).upper()

        mafia_count = ceil(len(accepted_User) / 5)
        mafias = []
        to_select = accepted_User.copy()

        for x in range(mafia_count):
            f = random.choice(to_select)
            mafias.append(f)
            to_select.remove(f)

        print("Not Mafia: ", to_select)
        print("Mafias: ", mafias)

        guild = ctx.message.guild

        for count, x in enumerate(range(len(mafias))):
            await guild.create_text_channel(f'mafia{count + 1}')

        for count, x in enumerate(range(len(to_select))):
            await guild.create_text_channel(f'person{count + 1}')

        f = """
        
        first_message = await ctx.send("Hallo, wer möchte mitspielen?")

        author = ctx.message.author
        author_voice_channel = ctx.message.author.voice.channel

        play_all = False

        for emoji in ('👍', '👎'):
            await first_message.add_reaction(emoji)

        def check(reaction, user):
            return user == author and str(reaction.emoji) in ['👍', '👎']

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)

        except asyncio.TimeoutError:
            await ctx.send('👎')
        else:
            if reaction.emoji == '👍':
                play_all = True

        print(play_all)
        """


def setup(bot):
    bot.add_cog(Basic(bot))
