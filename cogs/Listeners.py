import discord

from datetime import date
from cogs.ranking import Ranking
from itertools import cycle
from discord.ext.commands import CommandNotFound, MissingPermissions
from discord.ext.commands.errors import MemberNotFound, RoleNotFound, NotOwner
from etc.sql_reference import database_setup, log_message, get_user_voice_time, get_server, get_welcome_role
from etc.sql_reference import change_msg_welcome_channel, setup_config, add_user_voice_time, deactivate_guild
from etc.sql_reference import get_prefix, get_disabled_commands, get_welcome_message, get_welcome_channel
from etc.sql_reference import insert_user_voice_time, get_main_channel, get_invites_to_user, log_invite, activate_guild
from etc.error_handling import invalid_argument
from discord.ext import tasks, commands
from time import perf_counter


class Listeners(commands.Cog):
    def __init__(self, bot):
        self.voice_track = {}
        self.invites = {}
        self.bot = bot
        self.ranking = Ranking(bot)
        self.status = cycle(['Aktuell in Arbeit!', 'Von Ramo programmiert!', 'Noch nicht fertig!'])

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not before.channel and after.channel:
            self.voice_track[str(member)] = perf_counter()

        elif before.channel and not after.channel:
            try:
                time = self.voice_track[str(member)] - perf_counter()

                if round(time * -1) <= 60:
                    return

                await self.ranking.add_xp(self, member, member, round(round(time * -1) * 0.05), member.guild.id)

                minutes = int(round(time * - 1) / 60)

                if get_user_voice_time(member):
                    add_user_voice_time(member, minutes)

                else:
                    insert_user_voice_time(member, minutes)

            except KeyError:
                pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        main_channel = await get_main_channel(guild)
        if get_server(guild.id):
            activate_guild(guild.id)
        else:
            setup_config(guild.id, main_channel, main_channel)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        deactivate_guild(guild.id)

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
        role = get_welcome_role(ctx.guild)

        await ctx.add_roles(role)

        channel = await get_welcome_channel(ctx.guild)

        invites_before_join = self.invites[ctx.guild.id]
        invites_after_join = await ctx.guild.invites()

        for invite in invites_before_join:
            if invite.uses < self.find_invite_by_code(invites_after_join, invite.code).uses:
                welcome_message = get_welcome_message(ctx.guild.id)

                await channel.send(welcome_message)

                self.invites[ctx.guild.id] = invites_after_join

                if len(get_invites_to_user(ctx.guild.id, ctx)) == 0:
                    log_invite(ctx.guild.id, datum, str(invite.inviter), str(ctx))
                    await self.ranking.add_xp(self, ctx, invite.inviter, 200, ctx.guild.id)

        await self.ranking.add_xp(self, ctx, ctx, 20, ctx.guild.id)

    @commands.Cog.listener()
    async def on_member_remove(self, ctx):
        try:
            self.invites[ctx.guild.id] = await ctx.guild.invites()
        except:
            pass

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return

        prefix = get_prefix(ctx.guild.id)
        log_message(ctx.guild.id, str(date.today()), ctx)

        ctx.content = ctx.content.replace(prefix, self.bot.command_prefix)

        if str(ctx.content).startswith(self.bot.command_prefix):
            disabled_commands = get_disabled_commands(ctx.guild.id)
            if ctx.content.replace(self.bot.command_prefix, "") not in disabled_commands:
                await ctx.add_reaction("🔁")
                await self.bot.process_commands(ctx)
                if str(ctx.content) != self.bot.command_prefix + "stats" and str(ctx.content).replace(self.bot.command_prefix, "") in self.bot.user_commands:
                    await self.ranking.add_xp(self, ctx, ctx.author, 25, ctx.guild.id)
        else:
            await self.ranking.add_xp(self, ctx, ctx.author, 5, ctx.guild.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        prefix = get_prefix(payload.guild_id)
        if str(payload.member) == str(self.bot.user):
            return

        if str(payload.event_type) == "REACTION_ADD" and str(payload.emoji) == "🔁":
            guild = self.bot.get_guild(payload.guild_id)
            message = await discord.utils.get(guild.channels, id=payload.channel_id).fetch_message(payload.message_id)

            if str(message.author) == str(payload.member):
                message.content = message.content.replace(prefix, self.bot.command_prefix)
                if message.content != self.bot.command_prefix + "stats":
                    await self.ranking.add_xp(self, discord.utils.get(guild.channels, id=payload.channel_id),
                                              message.author, 25, payload.guild_id)
                await self.bot.process_commands(message)

    @tasks.loop(seconds=10)
    async def change_status(self):
        await self.bot.change_presence(activity=discord.Game(next(self.status)))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            return await ctx.send(":question: Unbekannter Befehl :question:")

        elif isinstance(error, MissingPermissions) or isinstance(error, NotOwner):
            return await ctx.send(":hammer: Du bist leider nicht berechtigt diesen Command zu nutzen. :hammer:")

        elif isinstance(error, MemberNotFound) or isinstance(error, RoleNotFound):
            return await invalid_argument(ctx, ctx.message.content.split()[0].replace(self.bot.command_prefix, ""))

        raise error


def setup(bot):
    bot.add_cog(Listeners(bot))
