import requests
import discord

from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageOps
from discord.ext import commands
from sql.config import get_main_channel
from sql.level import get_server_ranks, get_xp_from_user, insert_user_xp, update_user_xp


class Ranking(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ranking(self, ctx):
        try:
            server_ranks = get_server_ranks(ctx.guild.id)

            data = [(server_ranks[1], await self.xp_lvl(server_ranks[2])) for server_ranks in server_ranks[::-1]]

            embed = discord.Embed(title="Ranklist", description="List of Top 5 Server Ranks", color=0x1acdee)
            embed.set_author(name="Zemo Bot",
                             icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

            for user in range(5):
                embed.add_field(name=f"{data[user][0]}", value=f"Rank: {data[user][1]}", inline=False)

            await ctx.send(embed=embed)

        except:
            await ctx.send("Bisher sind leider nicht genügend Daten vorhanden.")

    @commands.command()
    async def stats(self, ctx, member: discord.Member = 0):
        async def create_level_image(ctx, name, url, level, rank):
            colors = {range(0, 10): (155, 155, 155), range(10, 20): (192, 41, 66), range(20, 30): (217, 91, 67),
                      range(30, 40): (254, 204, 35), range(40, 50): (70, 122, 60), range(50, 60): (78, 141, 219),
                      range(60, 70): (118, 82, 201), range(70, 80): (194, 82, 201), range(80, 90): (84, 36, 55),
                      range(90, 100): (153, 124, 82)}

            for color_range in colors:
                if level <= 100 and level in color_range:
                    color = colors[color_range]
                    break
                elif 1000 > level > 100 and level - int(str(level)[0]) * 100 in color_range:
                    color = colors[color_range]
                    break
            else:
                color = (155, 155, 155),

            role = ctx.message.author.roles

            xp_current_lvl = await self.lvl_xp(level)
            xp_next_lvl = await self.lvl_xp(level + 1)
            xp_current = get_xp_from_user(ctx.guild.id, name.id)

            step = xp_next_lvl - xp_current_lvl
            state = xp_current - xp_current_lvl

            try:
                img = Image.open(r'img/stats/bg{}.png'.format(round(round(state / step * 100) / 2)))
            except:
                img = Image.open(r'img/stats/bg0.png')

            response = requests.get(url)
            pb = Image.open(BytesIO(response.content))
            img = ImageOps.scale(img, factor=2)
            img = ImageOps.expand(img, border=150, fill="black")

            pb = pb.resize((456, 430), Image.ANTIALIAS)
            pb = ImageOps.expand(pb, border=15, fill=f'{max(role).colour}')

            img.paste(pb, (130, 75))

            xp_string = f"XP: {xp_current} / {xp_next_lvl}"

            # Font Positions
            level_positions = {1: (410, 585), 2: (355, 585), 3: (300, 585), 4: (230, 585)}
            nxt_level_positions = {1: (1720, 585), 2: (1705, 585), 3: (1700, 585), 4: (1700, 585)}

            # Draw Name
            draw = ImageDraw.Draw(img)
            name_level_size = 130 if len(str(name)) <= 19 else 130 - (len(str(name)) - 19) * 5
            draw.text((680, 175), f"Rank: #{rank} Level: {level}", color, font=ImageFont.truetype('fonts/micross.ttf', name_level_size))
            draw.text((680, 330), f"{name}", color, font=ImageFont.truetype('fonts/micross.ttf', name_level_size))

            # Draw Lvl
            draw.text(level_positions[len(str(level))], f"{level}", color,
                      font=ImageFont.truetype('fonts/micross.ttf', 130))
            draw.text(nxt_level_positions[len(str(level))], f"{level + 1}", color,
                      font=ImageFont.truetype('fonts/micross.ttf', 130))

            # Draw XP
            xp_position = (830 - int((int(len(xp_string) - 12) * 25)), 775)
            draw.text(xp_position, xp_string, (68, 180, 132), font=ImageFont.truetype('fonts/CORBEL.TTF', 115))

            with BytesIO() as output:
                img.save(output, format="PNG")
                output.seek(0)
                await ctx.send(file=discord.File(fp=output, filename="image.png"))

        if not member:
            level = await self.get_lvl(ctx, ctx.author)
            rank = await self.get_rank(ctx, ctx.author)
            await create_level_image(ctx, ctx.author, ctx.author.avatar_url, level, rank)
        else:
            level = await self.get_lvl(ctx, member)
            rank = await self.get_rank(ctx, member)
            await create_level_image(ctx, member, member.avatar_url, level, rank)

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

    async def set_xp(self, ctx, user: discord.Member, amout):
        update_user_xp(ctx.guild.id, user, amout)

    async def add_xp(self, ctx, user, xp, guild_id):
        if isinstance(user, str):
            try:
                member = ctx.author
            except:
                member = ctx
        else:
            member = user

        user = user
        user_xp = get_xp_from_user(guild_id, user.id)

        if user_xp:
            old_level = await self.xp_lvl(user_xp)
            new_level = await self.xp_lvl(user_xp + int(xp))

            insert_user_xp(guild_id, user.id, xp)

        else:
            old_level = 0
            new_level = await self.xp_lvl(int(xp))

            insert_user_xp(guild_id, user.id, xp)

        if old_level != new_level:
            channel = await get_main_channel(ctx)
            await channel.send(f"Gratuliere {member.mention}, du bist zu Level {new_level} aufgestiegen!  :partying_face:  :partying_face: ")

    async def get_lvl(self, ctx, user):
        return await self.xp_lvl(get_xp_from_user(ctx.guild.id, user.id))

    async def get_rank(self, ctx, user):
        ordered_list = get_server_ranks(ctx.guild.id)[::-1]
        x = [count + 1 for count, x in enumerate(ordered_list) if ordered_list[count][1] == user]
        return x[0] if x else "Bot"

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

            if i <= xp < i + increment:
                level_person = level

            i += increment
            j += 1

        return level_person


def setup(bot):
    bot.add_cog(Ranking(bot))
