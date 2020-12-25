from io import BytesIO
from PIL import Image, ImageFont, ImageDraw, ImageOps
from discord.ext import commands
from etc.global_functions import get_main_channel
import requests
import discord
import sqlite3


class Ranking(commands.Cog):
    def __init__(self, bot):
        self.conn_main = sqlite3.connect("main.db")
        self.cur_main = self.conn_main.cursor()
        self.bot = bot

    @commands.is_owner()
    @commands.command()
    async def setup_db(self, ctx):
        for user in ctx.guild.users:
            self.cur_main.execute("INSERT INTO LEVEL (server, user, xp) VALUES (?,?,?)",
                                  ([ctx.guild.id, str(user), 20]))
            self.conn_main.commit()

    @commands.command()
    async def rank(self, ctx):
        try:
            self.cur_main.execute("SELECT * FROM LEVEL WHERE server=? ORDER BY xp ASC", ([str(ctx.guild.id)]))
            x = self.cur_main.fetchall()

            data = [(x[1], await self.xp_lvl(x[2])) for x in x[::-1]]

            embed = discord.Embed(title="Ranklist", description="List of Top 5 Server Ranks", color=0x1acdee)
            embed.set_author(name="Zemo Bot",
                             icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")

            for x in range(5):
                embed.add_field(name=f"{data[x][0]}", value=f"Rank: {data[x][1]}", inline=False)
            await ctx.send(embed=embed)

        except:
            await ctx.send("Bisher sind leider nicht genügend Daten vorhanden.")

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
            state = xp_current - xp_current_lvl + 25

            try:
                img = Image.open(r'bg/bg{}.png'.format(round(round(state / step * 100) / 2)))
            except:
                img = Image.open(r'bg/bg0.png')

            response = requests.get(url)
            pb = Image.open(BytesIO(response.content))
            img = ImageOps.scale(img, factor=2)
            img = ImageOps.expand(img, border=150, fill="black")

            pb = pb.resize((456, 430), Image.ANTIALIAS)
            pb = ImageOps.expand(pb, border=15, fill=f'{max(role).colour}')

            img.paste(pb, (130, 75))

            # Create Font
            font = ImageFont.truetype('fonts/CORBEL.TTF', 115)
            font_lvl = ImageFont.truetype('fonts/micross.ttf', 130)

            # Print Name
            draw = ImageDraw.Draw(img)
            draw.text((760, 130), f"Level: {level}\nRank: #{rank}\n{name}", (26, 205, 238), font=font_lvl)
            # draw.text((650, 350), name, (68, 180, 132), font=font)

            # Print Lvl
            level_show = draw.text((100, 585), f"Level: {level}", (26, 205, 238), font=font_lvl)
            nxt_level_show = draw.text((1950, 585), f"{level + 1}", (26, 205, 238), font=font_lvl)

            # Print XP
            level_show = draw.text((830, 775), f"XP: {xp_current + 25} / {xp_next_lvl}", (68, 180, 132), font=font)

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

    @commands.is_owner()
    @commands.command()
    async def add_xp(self, ctx, user, xp):
        async def get_xp(ctx, user):
            exp = self.cur_main.execute("SELECT * FROM LEVEL WHERE server=? AND user=?",
                                        ([str(ctx.guild.id), str(user)]))
            x = self.cur_main.fetchall()
            if x:
                return (x[0][2])
            else:
                return 0

        async def xp_lvl(xp):
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

        try:
            member = ctx.author
        except:
            member = ctx

        user = str(user)
        self.cur_main.execute("SELECT * FROM LEVEL WHERE server=? AND user=?", ([str(ctx.guild.id), user]))
        x = self.cur_main.fetchall()

        if x:
            old_level = await xp_lvl(x[0][2])
            new_level = await xp_lvl(int(await get_xp(ctx, user)) + int(xp))

            new_xp = int(await get_xp(ctx, user)) + int(xp)
            sql = "UPDATE LEVEL SET xp=? WHERE server=? AND user=?"
            val_1 = (new_xp, str(ctx.guild.id), str(user))

            self.cur_main.execute(sql, val_1)
            self.conn_main.commit()
        else:
            old_level = 0
            new_level = await xp_lvl(int(xp))

            sql = "INSERT INTO LEVEL (server, user, xp) VALUES (?, ?, ?)"
            val_1 = (str(ctx.guild.id), str(user), int(xp))

            self.cur_main.execute(sql, val_1)
            self.conn_main.commit()

        if old_level != new_level:
            channel = await get_main_channel(ctx)
            await channel.send(f"Gratuliere {member.mention}, du bist zu Level {new_level} aufgestiegen!  :partying_face:  :partying_face: ")

    async def get_xp(self, ctx, user):
        self.cur_main.execute("SELECT * FROM LEVEL WHERE server=? AND user=?", ([str(ctx.guild.id), str(user)]))
        x = self.cur_main.fetchall()
        if x:
            return (x[0][2])
        else:
            return 0

    async def get_lvl(self, ctx, user):
        return await self.xp_lvl(await self.get_xp(ctx, user))

    @commands.command()
    async def get_rank(self, ctx, user):
        self.cur_main.execute("SELECT * FROM LEVEL WHERE server=? ORDER BY xp ASC", ([str(ctx.guild.id)]))
        ordered_list = self.cur_main.fetchall()[::-1]
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

            if xp >= i and xp < i + increment:
                level_person = level

            i += increment
            j += 1

        return level_person


def setup(bot):
    bot.add_cog(Ranking(bot))
