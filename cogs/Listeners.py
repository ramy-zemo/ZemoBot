import discord

from datetime import date
from cogs.ranking import Ranking
from itertools import cycle
from discord.ext.commands import CommandNotFound, MissingPermissions
from discord.ext.commands.errors import MemberNotFound, RoleNotFound, NotOwner

from etc.error_handling import invalid_argument
from discord.ext import tasks, commands
from time import perf_counter

from etc.sql_config import get_welcome_role, get_main_channel


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

                self.bot.ApiClient.request(self.bot.ApiClient.add_user_voice_time,
                                           params={"guild_id": member.guild.id,
                                                   "user_id": member.id, "minutes": minutes})
            except KeyError:
                pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        main_channel = await get_main_channel(self.bot.ApiClient, guild)

        if self.bot.ApiClient.request(self.bot.ApiClient.check_server_status, params={"guild_id": guild.id}):
            self.bot.ApiClient.request(self.bot.ApiClient.activate_guild, params={"guild_id": guild.id})
        else:
            self.bot.ApiClient.request(self.bot.ApiClient.setup_config, params={"guild_id": guild.id,
                                                                                "main_channel_id": main_channel.id,
                                                                                "welcome_channel_id": main_channel.id})

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        self.bot.ApiClient.request(self.bot.ApiClient.deactivate_guild, params={"guild_id": guild.id})

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

        channel = await get_main_channel(self.bot.ApiClient, ctx.guild)

        invites_before_join = self.invites[ctx.guild.id]
        invites_after_join = await ctx.guild.invites()

        for invite in invites_before_join:
            if invite.uses < self.find_invite_by_code(invites_after_join, invite.code).uses:
                welcome_message = self.bot.ApiClient.request(self.bot.ApiClient.get_welcome_message,
                                                             params={"guild_id": ctx.guild.id})
                default_welcome_message = f'Selam {ctx.mention}, willkommen in der Familie!\nHast du Ärger, gehst du Cafe Al Zemo, gehst du zu Ramo!\nEingeladen von: {invite.inviter.mention}'

                if welcome_message:
                    await channel.send(welcome_message.format(member=ctx.mention, inviter=invite.inviter.mention))
                else:
                    await channel.send(default_welcome_message)

                self.invites[ctx.guild.id] = invites_after_join
                invites_to_user = self.bot.ApiClient.request(self.bot.ApiClient.get_invites_to_user,
                                                             params={"guild_id": ctx.guild.id, "user_id": ctx.id})

                if len(invites_to_user) == 0:
                    self.bot.ApiClient.request(self.bot.ApiClient.log_invite,
                                               params={"guild_id": ctx.guild.id,
                                                       "date": datum,
                                                       "from_user_id": invite.inviter.id,
                                                       "to_user_id": ctx.id})

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

        prefix = self.bot.ApiClient.request(self.bot.ApiClient.get_prefix, params={"guild_id": ctx.guild.id})
        self.bot.ApiClient.request(self.bot.ApiClient.log_message,
                                   params={"guild_id": ctx.guild.id,
                                           "date": str(date.today()),
                                           "user_id": ctx.author.id,
                                           "message": ctx.content})

        ctx.content = ctx.content.replace(prefix, self.bot.command_prefix)
        if str(ctx.content).startswith(self.bot.command_prefix):
            command = ctx.content.replace(self.bot.command_prefix, "").split()[0]
            command_is_valid = self.bot.ApiClient.request(self.bot.ApiClient.check_command_status_for_guild,
                                                          params={"guild_id": ctx.guild.id, "command": command})
            all_admin_commands = self.bot.ApiClient.request(self.bot.ApiClient.get_all_admin_commands)

            if command_is_valid:
                await ctx.add_reaction("🔁")
                await self.bot.process_commands(ctx)
                guild_commands_and_category = self.bot.ApiClient.request(self.bot.ApiClient.get_all_guild_commands_and_category,
                                                                         params={"guild_id": ctx.guild.id})

                if str(ctx.content) != self.bot.command_prefix + "stats" and str(ctx.content).replace(self.bot.command_prefix, "").split()[0] in guild_commands_and_category:
                    await self.ranking.add_xp(ctx, ctx.author, 25, ctx.guild.id)

            elif ctx.author.id in self.bot.admin_ids and ctx.content.replace(self.bot.command_prefix, "").split()[0] in all_admin_commands:
                await ctx.add_reaction("🔁")
                await self.bot.process_commands(ctx)

            else:
                return await ctx.send(":question: Unbekannter Befehl :question:")

        else:
            await self.ranking.add_xp(ctx, ctx.author, 5, ctx.guild.id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        prefix = self.bot.ApiClient.request(self.bot.ApiClient.get_prefix, params={"guild_id": payload.guild_id})
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
        self.bot.logger.error(str(error))

        if isinstance(error, CommandNotFound):
            return await ctx.send(":question: Unbekannter Befehl :question:")

        elif isinstance(error, MissingPermissions) or isinstance(error, NotOwner):
            return await ctx.send(":hammer: Du bist leider nicht berechtigt diesen Command zu nutzen. :hammer:")

        elif isinstance(error, MemberNotFound) or isinstance(error, RoleNotFound):
            return await invalid_argument(self, ctx, ctx.message.content.split()[0].replace(self.bot.command_prefix, ""))

        # elif isinstance(error, CommandInvokeError):
            # print(error)
            # return await ctx.send(":hammer: Ich bin leider nicht berechtigt hier Nachrichten zu schreiben. :hammer:")

        raise error


def setup(bot):
    bot.add_cog(Listeners(bot))
