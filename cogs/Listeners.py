import discord

from datetime import date
from cogs.ranking import Ranking
from itertools import cycle
from discord.ext.commands import CommandNotFound, MissingPermissions
from discord.ext.commands.errors import MemberNotFound, RoleNotFound, NotOwner, CommandInvokeError
from sql.message import log_message
from sql.commands import get_all_guild_commands_and_category
from sql.disabled_commands import check_command_status_for_guild
from sql.sql_config import get_server, get_welcome_role, get_prefix, get_welcome_message, setup_config
from sql.sql_config import activate_guild, deactivate_guild, get_main_channel
from sql.voice import add_user_voice_time
from sql.invites import get_invites_to_user, log_invite
from sql.admin_commands import get_all_admin_commands
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

                await self.ranking.add_xp(member, member, round(round(time * -1) * 0.05), member.guild.id)
                minutes = int(round(time * - 1) / 60)
                add_user_voice_time(member.guild.id, member.id, minutes)

            except KeyError:
                pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        main_channel = await get_main_channel(guild)

        if get_server(guild.id):
            activate_guild(guild.id)
        else:
            setup_config(guild.id, main_channel.id, main_channel.id)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        deactivate_guild(guild.id)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            self.invites[guild.id] = await guild.invites()

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

        if role:
            await ctx.add_roles(role)

        channel = await get_main_channel(ctx.guild)

        invites_before_join = self.invites[ctx.guild.id]
        invites_after_join = await ctx.guild.invites()

        for invite in invites_before_join:
            if invite.uses < self.find_invite_by_code(invites_after_join, invite.code).uses:
                welcome_message = get_welcome_message(ctx.guild.id)
                default_welcome_message = f'Selam {ctx.mention}, willkommen in der Familie!\nHast du Ärger, gehst du Cafe Al Zemo, gehst du zu Ramo!\nEingeladen von: {invite.inviter.mention}'

                if welcome_message:
                    await channel.send(welcome_message.format(member=ctx.mention, inviter=invite.inviter.mention))
                else:
                    await channel.send(default_welcome_message)
                self.invites[ctx.guild.id] = invites_after_join

                if len(get_invites_to_user(ctx.guild.id, ctx.id)) == 0:
                    log_invite(ctx.guild.id, datum, invite.inviter.id, ctx.id)
                    if str(invite.inviter) != str(self.bot.user):
                        await self.ranking.add_xp(ctx, invite.inviter.id, 200, ctx.guild.id)

        await self.ranking.add_xp(ctx, ctx, 20, ctx.guild.id)

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

        if isinstance(ctx.channel, discord.DMChannel):
            return await ctx.channel.send("Aktuell sind Commands nicht per DM möglich.")

        prefix = get_prefix(ctx.guild.id)
        log_message(ctx.guild.id, str(date.today()), ctx.author.id, ctx.content)

        ctx.content = ctx.content.replace(prefix, self.bot.command_prefix)
        if str(ctx.content).startswith(self.bot.command_prefix):
            if check_command_status_for_guild(ctx.guild.id, ctx.content.replace(self.bot.command_prefix, "").split()[0]):
                await ctx.add_reaction("🔁")
                await self.bot.process_commands(ctx)
                if str(ctx.content) != self.bot.command_prefix + "stats" and str(ctx.content).replace(self.bot.command_prefix, "").split()[0] in get_all_guild_commands_and_category(ctx.guild.id):
                    await self.ranking.add_xp(ctx, ctx.author, 25, ctx.guild.id)

            elif ctx.author.id in self.bot.admin_ids and ctx.content.replace(self.bot.command_prefix, "").split()[0] in get_all_admin_commands():
                await ctx.add_reaction("🔁")
                await self.bot.process_commands(ctx)

        else:
            await self.ranking.add_xp(ctx, ctx.author, 5, ctx.guild.id)

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
                    await self.ranking.add_xp(discord.utils.get(guild.channels, id=payload.channel_id),
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

        # elif isinstance(error, CommandInvokeError):
            # print(error)
            # return await ctx.send(":hammer: Ich bin leider nicht berechtigt hier Nachrichten zu schreiben. :hammer:")

        raise error


def setup(bot):
    bot.add_cog(Listeners(bot))
