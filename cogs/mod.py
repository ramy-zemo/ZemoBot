import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from etc.error_handling import invalid_argument


class Auszeit(commands.Cog):
    def __init__(self, bot):
        self.timeout_roles = [768172546860253194, 768172546104229899]
        self.bot = bot

    @commands.command()
    async def amo(self, ctx, *args):
        y = [mem for mem in [m for m in ctx.guild.members if m != ctx.message.author] if "AMO" in [x.name for x in mem.roles]]

        for x in y:
            await x.send("{}".format(" ".join(args)))

    @has_permissions(create_instant_invite=True)
    @commands.command()
    async def invite(self, ctx, max_age=0, max_uses=0, temporary=False, unique=False, reason="", ):
        await ctx.send(
            await ctx.channel.create_invite(max_age=max_age, max_uses=max_uses, temporary=temporary, unique=unique,
                                            reason=reason))

    @has_permissions(kick_members=True)
    @commands.command()
    async def auszeit(self, ctx, member: discord.Member, *args):
        non_removable_roles = [discord.utils.get(ctx.message.guild.roles, name="Server Booster"),
                               discord.utils.get(ctx.message.guild.roles, name="@everyone")]

        author_roles = ctx.message.author.roles
        timeout_roles = [discord.utils.get(ctx.message.guild.roles, id=x) for x in self.timeout_roles]
        voice_before_game = []
        if any([True for x in author_roles if x in timeout_roles]):
            users_to_timeout = member
            seconds_to_kick = int(args[0])

            if seconds_to_kick < 30:
                return await invalid_argument(ctx, "auszeit")

            banned_role = await ctx.message.guild.create_role(name="banned")
            await banned_role.edit(colour=0xff0000)

            overwrites_auszeit = {
                ctx.message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                banned_role: discord.PermissionOverwrite(read_messages=True, read_message_history=True)
            }

            auszeit_channel = await ctx.message.guild.create_text_channel('auszeit', overwrites=overwrites_auszeit)

            voice_channel = await ctx.message.guild.create_voice_channel('auszeit', overwrites=overwrites_auszeit)

            # Check if User is in Voice channel
            in_voice = users_to_timeout.voice
            if in_voice is not None:
                voice_before_game.append(ctx.message.author.voice.channel)
                await users_to_timeout.edit(voice_channel=voice_channel)

            # Delete old Roles and save them
            roles_before = {}
            real_role = []

            for role in users_to_timeout.roles:
                if role not in non_removable_roles:
                    real_role.append(role)

            roles_before[users_to_timeout] = real_role

            await users_to_timeout.remove_roles(*real_role)
            await users_to_timeout.add_roles(discord.utils.get(ctx.message.guild.roles, name="banned"))

            await asyncio.sleep(5)

            await auszeit_channel.send("https://www.youtube.com/watch?v=NPvFkXVi5mM")

            embed = discord.Embed(title="Auszeit", color=0xff0000)
            embed.set_author(name="Zemo Bot",
                             icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
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

    @has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, member: discord.Member):
        try:
            await ctx.guild.kick(member)
        except discord.errors.Forbidden:
            return await ctx.send("Ich habe leider nicht die notwendige Berechtigung. " + ctx.author.mention)

        await ctx.send(ctx.message.author.mention + f" Habebe ist erledigt. {member} wurde gekickt.")

    @has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, member: discord.Member):
        try:
            await ctx.guild.ban(member)
        except discord.errors.Forbidden:
            return await ctx.send("Ich habe leider nicht die notwendige Berechtigung. " + ctx.author.mention)
        await ctx.send(ctx.message.author.mention + f" Habebe ist erledigt. {member} wurde gebannt.")

    @has_permissions(ban_members=True)
    @commands.command()
    async def unban(self, ctx, *args):
        to_unban = ctx.guild.get_member(int(str(args[0]).strip("<>!@")))
        await ctx.guild.unban(to_unban)
        await ctx.send(ctx.message.author.mention + f"Habebe ist erledigt. {to_unban} wurde entbannt.")


def setup(bot):
    bot.add_cog(Auszeit(bot))
