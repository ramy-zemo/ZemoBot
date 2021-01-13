from discord.ext import tasks, commands
from time import perf_counter
import discord
from datetime import date
from cogs.ranking import Ranking
from itertools import cycle
from discord.ext.commands import CommandNotFound, MissingPermissions
from etc.sql_reference import database_setup, log_message, get_user_voice_time
from etc.sql_reference import change_msg_welcome_channel, setup_config, add_user_voice_time
from etc.sql_reference import insert_user_voice_time, get_main_channel, get_invites_to_user, log_invite
import sqlite3


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.voice_track = {}
        self.invites = {}
        self.bot = bot
        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()
        self.ranking = Ranking(bot)
        self.status = cycle(['Aktuell in Arbeit!', 'Von Ramo programmiert!', 'Noch nicht fertig!'])

    # Test On_Join
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not before.channel and after.channel:
            self.voice_track[str(member)] = perf_counter()

        elif before.channel and not after.channel:
            try:
                time = self.voice_track[str(member)] - perf_counter()

                if round(time * -1) <= 60:
                    return

                await self.ranking.add_xp(self, member, member, round(round(time * -1) * 0.05))

                minutes = int(round(time * - 1) / 60)

                if get_user_voice_time(member):
                    add_user_voice_time(member, minutes)

                else:
                    insert_user_voice_time(member, minutes)

            except KeyError:
                print("Join Time unknowwn")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        overwrites_main = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True,
                                                            send_messages=False)
        }

        # Check if Server is in Database
        result = get_main_channel(guild)

        if not result:
            main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)

            setup_config(guild, main_channel, main_channel)

        else:
            channel_id = result[0][0]
            channel = discord.utils.get(guild.channels, id=int(channel_id))

            if channel:
                print("Hinzugefügter Server schon in Datenbank")

            else:
                main_channel = await guild.create_text_channel(name="zemo bot", overwrites=overwrites_main)

                change_msg_welcome_channel(guild, main_channel, main_channel)


    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.invites[guild.id] = await guild.invites()

        database_setup()

        self.change_status.start()
        print("Bot {} läuft!".format(self.bot.user))

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
                    await channel.send(f'Selam {ctx.mention}, willkommen in der Familie!\nHast du Ärger, gehst du Cafe Al Zemo, gehst du zu Ramo!\n Eingeladen von: {invite.inviter.mention}')

                self.invites[ctx.guild.id] = invites_after_join

                if len(get_invites_to_user(ctx.guild.id, ctx)) == 0:
                    log_invite(ctx.guild.id, datum, str(invite.inviter), str(ctx))
                    await self.ranking.add_xp(self, ctx, invite.inviter, 200)

        await self.ranking.add_xp(self, ctx, ctx, 20)

    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        print(ctx)
        try:
            self.invites[ctx.guild.id] = await ctx.guild.invites()
        except:
            print("Error")

    @commands.Cog.listener()
    async def on_message(self, ctx):
        message = ctx

        if message.author == self.bot.user:
            return

        datum = str(date.today())
        log_message(ctx.guild.id, datum, message)

        if str(message.content).startswith("$"):
            await self.ranking.add_xp(self, ctx, message.author, 25)
        else:
            await self.ranking.add_xp(self, ctx, message.author, 5)

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.status)))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return await ctx.send(":question: Unbekannter Befehl :question:")

        elif isinstance(error, MissingPermissions):
            return await ctx.send(":hammer: Du bist leider nicht berechtigt diesen Command zu nutzen. :hammer:")

        raise error


def setup(bot):
    bot.add_cog(Listeners(bot))
