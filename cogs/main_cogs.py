from discord.ext import commands
import discord
import asyncio
from math import ceil
from datetime import date
import random
import requests
import sqlite3
import string
from bs4 import BeautifulSoup
import html
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageOps


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.invites = {}
        self.font_list = ['3-d', '3x5', '5lineoblique ', 'acrobatic', 'alligator', 'alligator2', 'alphabet', 'avatar',
                     'banner', 'banner3-D', 'banner3', 'banner4', 'barbwire', 'basic', 'bell', 'big', 'bigchief',
                     'binary', 'block', 'bubble', 'bulbhead', 'calgphy2', 'caligraphy', 'catwalk', 'chunky', 'coinstak',
                     'colossal', 'computer', 'contessa', 'contrast', 'cosmic', 'cosmike', 'cyberlarge', 'cybermedium',
                     'cybersmall', 'cygnet', 'diamond', 'digital', 'doh', 'doom', 'dotmatrix', 'drpepper', 'eftichess',
                     'eftifont', 'eftipiti', 'eftirobot', 'eftitalic ', 'eftiwall', 'eftiwater', 'epic', 'fender',
                     'fourtops', 'fuzzy', 'goofy', 'gothic', 'graffiti', 'hollywood',
                     'invita', 'isometric1', 'isometric2', 'isometric3', 'isometric4', 'italic', 'jazmine', 'kban',
                     'larry3d', 'lcd', 'lean', 'letters', 'linux', 'lockergnome', 'madrid', 'marquee', 'maxfour',
                     'mike', 'mini', 'mirror', 'nancyj-fancy', 'nancyj-underlined', 'nancyj', 'nipples', 'o8', 'ogre',
                     'pawp', 'peaks', 'pebbles', 'pepper', 'poison', 'puffy', 'pyramid', 'rectangles', 'relief',
                     'relief2', 'rev', 'roman', 'rot13', 'rounded', 'rowancap', 'rozzo', 'sblood', 'script', 'serifcap',
                     'shadow', 'short', 'slant', 'slide', 'slscript', 'small', 'smisome1', 'smkeyboard', 'smscript',
                     'smshadow', 'smslant', 'smtengwar', 'speed', 'stampatello', 'standard', 'starwars', 'stellar',
                     'stop', 'straight', 'swan', 'tanja', 'tengwar', 'term', 'thick', 'thin', 'threepoint', 'ticks',
                     'ticksslant', 'tinker-toy', 'tombstone', 'trek', 'twopoint', 'univers', 'usaflag', 'weird']
        self.timeout_roles = [768172546860253194, 768172546104229899]
        self.allowed_roles = [481248489238429727, 710895965761962104, 768176239495610398, 768172546860253194,
                              770040428496945173, 768172546104229899, 768176269916635176, 770331799246995508]
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

        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()

        with open("trashtalk.txt") as file:
            self.text = file.readlines()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        overwrites_main = {
           guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True, send_messages=False)
        }

        self.main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.invites[guild.id] = await guild.invites()

        print("Bot {} läuft!".format(self.bot.user))

        self.cur_main.execute('CREATE TABLE IF NOT EXISTS INVITES ( server TEXT, datum TEXT, von TEXT, an TEXT)')
        self.conn_main.commit()

        self.cur_main.execute('CREATE TABLE IF NOT EXISTS LEVEL ( server TEXT, user TEXT, xp INT)')
        self.conn_main.commit()

    def find_invite_by_code(self, invite_list, code):
        for inv in invite_list:
            if inv.code == code:
                return inv

    @commands.Cog.listener()
    async def on_member_join(self, ctx):
        datum = str(date.today())
        role = discord.utils.get(ctx.guild.roles, name="KANKA")

        await ctx.add_roles(role)

        channel = discord.utils.get(ctx.guild.channels, name="willkommen")

        invites_before_join = self.invites[ctx.guild.id]
        invites_after_join = await ctx.guild.invites()

        for invite in invites_before_join:

            if invite.uses < self.find_invite_by_code(invites_after_join, invite.code).uses:
                if channel is not None:
                    await channel.send(f'Selam {ctx.mention}, willkommen in der Familie!\nHast du Ärger, gehst du Cafe Al Zemo, gehst du zu Ramo!\nEingeladen von: {invite.inviter.mention}')

                self.invites[ctx.guild.id] = invites_after_join

                self.cur_main.execute("SELECT * FROM INVITES WHERE server = ? AND an=?", tuple([str(ctx.guild.id), str(ctx)]))

                if len(self.cur_main.fetchall()) == 0:
                    sql = "INSERT INTO INVITES (server, datum, von, an) VALUES (?, ?, ?, ?)"
                    val_1 = (ctx.guild.id, datum, str(invite.inviter), str(ctx))

                    self.cur_main.execute(sql, val_1)
                    self.conn_main.commit()
                    await self.add_xp(ctx, invite.inviter, 200)

        await self.add_xp(ctx, ctx, 20)

    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        self.invites[ctx.guild.id] = await ctx.guild.invites()

    @commands.Cog.listener()
    async def on_message(self, ctx):
        message = ctx
        if message.author == self.bot.user:
            return

        datum = str(date.today())

        self.cur_main.execute('CREATE TABLE IF NOT EXISTS Messages{} (server,  datum TEXT, von TEXT, nachricht TEXT)'.format(str(message.author.id)))
        self.conn_main.commit()

        sql = "INSERT INTO Messages{} (server, datum, von, nachricht) VALUES (?, ?, ?, ?)".format(str(message.author.id))
        val_1 = (ctx.guild.id, datum, str(message.author), str(message.content))

        self.cur_main.execute(sql, val_1)
        self.conn_main.commit()

        if str(message.content).startswith("$"):
            await self.add_xp(ctx, message.author, 25)
        else:
            await self.add_xp(ctx, message.author, 5)

    @commands.command()
    async def pb(self, ctx):
        await ctx.send(ctx.author.avatar_url)

    @commands.command()
    async def invites(self, ctx):
        self.cur_main.execute("SELECT * FROM INVITES WHERE server=? AND von=?", tuple([ctx.guild.id, str(ctx.message.author)]))

        embed = discord.Embed(title="Invites", description=f"Du hast bereits erfolgreich {len(self.cur_main.fetchall())} Personen eingeladen.", color=0x1acdee)
        embed.set_author(name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

        await ctx.send(embed=embed)

    @commands.command()
    async def stats(self, ctx):
        async def create_level_image(ctx, name, url, level, rank):
            user = name
            name = str(name)
            role = ctx.message.author.roles

            xp_current_lvl = await self.lvl_xp(level)
            xp_next_lvl = await self.lvl_xp(level + 1)
            xp_current = await self.get_xp(ctx, user)

            step = xp_next_lvl - xp_current_lvl
            state = xp_current - xp_current_lvl

            try:
                img = Image.open(r'E:\CodingProjects\Python Projects\DiscordBot\ZemoBot\bg\bg{}.png'.format(round(round(state / step * 100) / 2)))
            except:
                img = Image.open(r'E:\CodingProjects\Python Projects\DiscordBot\ZemoBot\bg\bg0.png')

            response = requests.get(url)
            pb = Image.open(BytesIO(response.content))
            img = ImageOps.scale(img, factor=2)
            img = ImageOps.expand(img, border=150, fill="black")

            pb = pb.resize((456, 430), Image.ANTIALIAS)
            pb = ImageOps.expand(pb, border=15, fill=f'{max(role).colour}')

            img.paste(pb, (130, 75))

            # Create Font
            font = ImageFont.truetype('CORBEL.TTF', 115)
            font_lvl = ImageFont.truetype('micross.ttf', 130)

            # Print Name
            draw = ImageDraw.Draw(img)
            draw.text((760, 130), f"Level: {level}\nRank: #{rank}\n{name}", (26, 205, 238), font=font_lvl)
            #draw.text((650, 350), name, (68, 180, 132), font=font)

            # Print Lvl
            level_show = draw.text((100, 585), f"Level: {level}", (26, 205, 238), font=font_lvl)
            nxt_level_show = draw.text((1950, 585), f"{level + 1}", (26, 205, 238), font=font_lvl)

            # Print XP
            level_show = draw.text((830, 775), f"XP: {xp_current} / {xp_next_lvl}", (68, 180, 132), font=font)

            with BytesIO() as output:
                img.save(output, format="PNG")
                output.seek(0)
                await ctx.send(file=discord.File(fp=output, filename="image.png"))

        level = await self.get_lvl(ctx, str(ctx.author))
        rank = await self.get_rank(ctx, str(ctx.author))
        await create_level_image(ctx, ctx.author, ctx.author.avatar_url, level, rank)

    async def lvl_xp(self, lvl):
        if lvl == 0:
            return 0
        increment = 100
        level = 0
        j = 1
        i = 100

        for x in range(100, 55000):
            level += 1

            if j == 10:
                j = 0
                increment += 100

            if level == lvl:
                return i

            i += increment
            j += 1

    async def xp_lvl(self, xp):
        level_person = 0
        increment = 100
        level = 0
        j = 1
        i = 100
        xp = int(xp)

        for x in range(100, 55000):
            level += 1

            if j == 10:
                j = 0
                increment += 100

            if xp >= i and xp < i + increment:
                level_person = level

            i += increment
            j += 1

        return level_person

    @commands.command()
    async def add_xp(self, ctx, user, xp):
        try:
            member = ctx.author
        except:
            member = ctx

        user = str(user)
        self.cur_main.execute("SELECT * FROM LEVEL WHERE server=? AND user=?", ([str(ctx.guild.id), user]))
        x = self.cur_main.fetchall()

        if x:
            old_level = await self.xp_lvl(x[0][2])
            new_level = await self.xp_lvl(int(await self.get_xp(ctx, user)) + int(xp))

            new_xp = int(await self.get_xp(ctx, user)) + int(xp)
            sql = "UPDATE LEVEL SET xp=? WHERE server=? AND user=?"
            val_1 = (new_xp, str(ctx.guild.id), str(user))

            self.cur_main.execute(sql, val_1)
            self.conn_main.commit()
        else:
            old_level = 0
            new_level = await self.xp_lvl(int(xp))

            sql = "INSERT INTO LEVEL (server, user, xp) VALUES (?, ?, ?)"
            val_1 = (str(ctx.guild.id), str(user), int(xp))

            self.cur_main.execute(sql, val_1)
            self.conn_main.commit()

        if old_level != new_level:
            await self.main_channel.send(f"Gratuliere {member.mention}, du bist zu Level {new_level} aufgestiegen!  :partying_face:  :partying_face: ")

    async def get_xp(self, ctx, user):
        exp = self.cur_main.execute("SELECT * FROM LEVEL WHERE server=? AND user=?", ([str(ctx.guild.id), str(user)]))
        x = self.cur_main.fetchall()
        if x:
            return (x[0][2])
        else:
            return 0

    async def get_lvl(self, ctx, user):
        return await self.xp_lvl(await self.get_xp(ctx, user))

    @commands.command()
    async def help(self, ctx, *args):
        embed = discord.Embed(title="Help", description="List of available commands", color=0x1acdee)
        embed.set_author(
            name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        embed.add_field(name="$trashtalk (*Mention)", value="Trashtalk people", inline=False)
        embed.add_field(name="$trashtalk_stats", value="Show your Discord Trashtalk Stats", inline=False)
        embed.add_field(name="$trashtalk_reset", value="Reset your Trashtalk Stats", inline=False)
        embed.add_field(name="$trashtalk_list", value="Show Trashtalk Words", inline=False)
        embed.add_field(name="$trashtalk_add", value="Add Words to trashtalk", inline=False)
        embed.add_field(name="$mafia (*mention)", value="Start Mafia Game", inline=False)
        embed.add_field(name="$ping", value="Check if bot is alive", inline=False)
        embed.add_field(name="$stats", value="Get your statistics", inline=False)
        embed.add_field(name="$auszeit (*mention) (*seconds)", value="Timeout Users", inline=False)
        embed.add_field(name="$meme", value="Return random meme", inline=False)
        embed.add_field(name="$font (*keyword) (font)", value="Returns ASCII Art, from provided Text.", inline=False)
        embed.add_field(name="$font_list", value="Get List of available Fonts.", inline=False)
        embed.add_field(name="$invites", value="List of your successful invites.", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def auszeit(self, ctx, *args):
        self.non_removable_roles = [discord.utils.get(ctx.message.guild.roles, name="Server Booster"),
                                    discord.utils.get(ctx.message.guild.roles, name="@everyone")]
        author_roles = ctx.message.author.roles
        timeout_roles = [discord.utils.get(ctx.message.guild.roles, id=x) for x in self.timeout_roles]
        voice_before_game = []
        if any([True for x in author_roles if x in timeout_roles]):
            users_to_timeout = ctx.message.guild.get_member(int(str(args[0]).strip("<>!@")))
            seconds_to_kick = int(args[1])

            if seconds_to_kick < 30:
                return await ctx.send("Eine Auszeit muss zumindest 30 Sekunden dauern.")

            self.auszeit_category = 769921393281466408
            banned_role = await ctx.message.guild.create_role(name="banned")
            await banned_role.edit(colour=0xff0000)

            overwrites_auszeit = {
                ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                banned_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True)
            }

            auszeit_channel = await ctx.message.guild.create_text_channel('auszeit', category=self.bot.get_channel(self.auszeit_category), overwrites=overwrites_auszeit)

            overwrites_voice = {
                ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                banned_role: discord.PermissionOverwrite(read_messages=True)
            }

            voice_channel = await ctx.message.guild.create_voice_channel('auszeit', category=self.bot.get_channel(
                self.auszeit_category), overwrites=overwrites_auszeit)

            # Check if User is in Voice channel
            in_voice = users_to_timeout.voice
            print(in_voice)
            if in_voice is not None:
                voice_before_game.append(ctx.message.author.voice.channel)
                await users_to_timeout.edit(voice_channel=voice_channel)

            # Delete old Roles and save them
            roles_before = {}
            real_role = []

            for f in users_to_timeout.roles:
                if f not in self.non_removable_roles:
                    real_role.append(f)

            roles_before[users_to_timeout] = real_role

            await users_to_timeout.remove_roles(*real_role)
            await users_to_timeout.add_roles(discord.utils.get(ctx.message.guild.roles, name="banned"))

            await asyncio.sleep(5)

            await auszeit_channel.send("https://www.youtube.com/watch?v=NPvFkXVi5mM")

            embed = discord.Embed(title="Auszeit", color=0xff0000)
            embed.set_author(
                name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
            embed.add_field(name="Deine Auszeit", value="Digga wie gehts auf der Stillen Treppe?", inline=False)
            embed.set_footer(text="Piss dich digga")
            await auszeit_channel.send(embed=embed)
            await auszeit_channel.send("Digga willkommen auf der Stillen Treppe." + users_to_timeout.mention)

            await asyncio.sleep(seconds_to_kick)

            await users_to_timeout.remove_roles(banned_role)
            await users_to_timeout.add_roles(*roles_before[users_to_timeout])

            if in_voice is not None:
                await users_to_timeout.edit(voice_channel=voice_before_game[0])

            await auszeit_channel.delete()
            await voice_channel.delete()

    @commands.command()
    async def voice_check(self, ctx, *args):
        await ctx.message.author.edit(voice_channel=None)

    @commands.command()
    async def kill(self, ctx, *args):
        users_to_kill = [ctx.message.guild.get_member(int(str(x).strip("<>!@"))) for x in args]

        while True:
            await users_to_kill[0].send("Du Hurensohn")

    @commands.command()
    async def trashtalk(self, ctx, *args):
        self.cur_main.execute('CREATE TABLE IF NOT EXISTS TrashTalk{} ( server TEXT, datum TEXT, von TEXT, an TEXT)'.format(
            str(ctx.message.author.id)))
        self.conn_main.commit()

        datum = str(date.today())

        sql = f"SELECT * FROM TrashTalk{str(ctx.message.author.id)}"

        self.cur_main.execute(sql)

        result = self.cur_main.fetchall()
        daten = [x[0] for x in result if x[0] == datum]

        if len(daten) < 10:
            users_to_tt = [ctx.message.guild.get_member(int(str(x).strip("<>!@"))) for x in args]
            for user in users_to_tt:
                sql = "INSERT INTO TrashTalk{} (server, datum, von, an) VALUES (?, ?, ?, ?)".format(str(ctx.message.author.id))
                val_1 = (str(ctx.guild.id), datum, str(ctx.message.author), str(user))

                self.cur_main.execute(sql,val_1)
                self.conn_main.commit()

                for t in self.text:
                    await user.send(t)
        else:
            await ctx.send(f"{ctx.message.author.mention} du hast dein Trash Limit für heute erreicht.")

    @commands.command()
    async def trashtalk_add(self, ctx, *args):
        with open("trashtalk.txt", "a") as file:
            file.write(" ".join(args) + "\n")

        await ctx.send("Nachricht erfolgreich hinzugefügt!")

    @commands.command()
    async def trashtalk_list(self, ctx):
        with open("trashtalk.txt", "r") as file:

            await ctx.message.author.send("```\n" + ''.join(file.readlines()) + "\n```")

    @commands.command()
    async def trashtalk_stats(self, ctx):
        datum = str(date.today())
        try:
            sql = f"SELECT * FROM TrashTalk{str(ctx.message.author.id)} WHERE server=?"
            val = ([str(ctx.guild.id)])
            self.cur_main.execute(sql, val)

            result = self.cur_main.fetchall()
            daten = [x[1] for x in result if x[1] == datum]

            await ctx.send(f"All time: {len(result)}, Today: {len(daten)}")

        except sqlite3.OperationalError:
            await ctx.send("Bisher sind keine Daten vorhanden.")

    @commands.command()
    async def trashtalk_reset(self, ctx, *args):
        try:
            self.cur_main.execute(f"DELETE FROM TrashTalk{str(ctx.message.author.id)} WHERE server=?", (str(ctx.guild.id)))
            self.conn_main.commit()
            await ctx.send(f"Trashtalk für {ctx.message.author.mention} erfolgreich zurückgesetzt.")
        except:
            await ctx.send(f"Nutzer {ctx.message.author.mention} nicht gefunden.")

    @commands.command()
    async def amo(self, ctx, *args):
        y = [mem for mem in [m for m in ctx.guild.members if m != ctx.message.author] if
             "AMO" in [x.name for x in mem.roles]]

        for x in y:
            await x.send("{}".format(" ".join(args)))

    @commands.command()
    async def testo(self, ctx, *args):
        return

    @commands.command()
    async def mafia(self, ctx, *args):
        guild = ctx.message.guild
        users_to_play = [guild.get_member(int(str(x).strip("<>!@"))) for x in args]
        self.non_removable_roles = [discord.utils.get(ctx.message.guild.roles, name="Server Booster"),
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
        game_id = ''.join(random.choice(string.ascii_letters) for x in range(6)).upper()

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
                if f not in self.non_removable_roles:
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
                name=''.join(random.choice(string.ascii_letters) for x in range(8)).upper())
            bot_created_roles.append(pp_role)

            overwrites_person = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                pp_role: discord.PermissionOverwrite(read_messages=True)
            }

            bot_created_channels.append(
                await guild.create_text_channel(f'person {game_id}', overwrites=overwrites_person,
                                                category=game_category))

            new_roles[x] = pp_role
            user = random.choice(to_select)
            await user.add_roles(pp_role)
            to_select.remove(user)

        mafia_role = await guild.create_role(
            name=''.join(random.choice(string.ascii_letters) for x in range(8)).upper())

        bot_created_roles.append(mafia_role)

        overwrites_mafia_channel = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            mafia_role: discord.PermissionOverwrite(read_messages=True)
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

        embed.add_field(name="Mitspieler:", value="\n" + ' '.join(
            [x.mention for x in accepted_user]), inline=True)

        await game_text_channel.send(embed=embed)

        # Game Body
        users_to_play = accepted_user.copy()

        while True:
            # Check if Game is still running
            if len(vote_mafias) < len(vote_persons) and len(vote_mafias) != 0:
                await asyncio.sleep(300)
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

                await self.delete_unwanted_channels(ctx, False)
                await self.delete_unwanted_roles(ctx, False)
                await ctx.send(f"Spiel {game_id} beendet")
                break

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
        await ctx.send(f'Pong!  :ping_pong:  In {round(self.bot.latency * 1000)}ms')

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

    @commands.command()
    async def embed(self, ctx, *args):
        embed = discord.Embed(title="Einladung",
                              description="Einladung erfolgreich angenommen.\n"
                                          "Das Spiel startet in kürze.",
                              color=0x00f030)

        embed.set_author(name="Zemo Bot",
                         icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def delete(self, ctx, *args):
        await self.delete_unwanted_roles(ctx)
        await self.delete_unwanted_channels(ctx)

    @commands.command()
    async def meme(self, ctx, *args):
        try:
            await ctx.send(requests.get("https://meme-api.herokuapp.com/gimme").json()["url"])
        except:
            await ctx.send("Die Meme API ist aktuell nicht verfügbar.")

    @commands.command()
    async def font_list(self, ctx):
        await ctx.message.author.send("```" + "\n".join(self.font_list) + "```")

    @commands.command()
    async def font(self, ctx, keyword=None, font=None,):
        if not keyword:
            embed = discord.Embed(title="Du musst ein Keyword angeben",
                                  description="Wenn du dir nicht sicher bist wie du diesen Befehl verwendest, nutze $help.",
                                  color=0xf00000)

            embed.set_author(name="Zemo Bot",
                             icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

            return await ctx.send(embed=embed)

        if not font:
            font = random.choice(self.font_list)

        request = requests.get(
            f"http://www.network-science.de/ascii/ascii.php?TEXT={keyword}&x=30&y=11&FONT={font}&RICH=no&FORM=left&STRE=no&WIDT=80")

        soup = BeautifulSoup(request.content, "html.parser")

        text = html.unescape(str(soup.find_all("pre")[1]))

        text_ascii = "\n".join(text.split("\n")[1:-1])

        text_discord = "```\n" + text_ascii +  f"\n\nFont: {font} , Keyword: {keyword}" +"```"

        await ctx.send(text_discord)

    @commands.command()
    async def get_rank(self, ctx, user):
        self.cur_main.execute("SELECT * FROM LEVEL WHERE server=? ORDER BY xp ASC", ([str(ctx.guild.id)]))
        ordered_list = self.cur_main.fetchall()[::-1]
        x = [count + 1 for count, x in enumerate(ordered_list) if ordered_list[count][1] == user]

        return x[0] if x else "Bot"


def setup(bot):
    bot.add_cog(Basic(bot))
