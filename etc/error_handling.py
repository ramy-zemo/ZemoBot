from discord import Embed
from sql.config import get_prefix
from config import ICON_URL


async def invalid_argument(ctx, command):
    commands = {"trashtalk_stats": "(member)",
                "trashtalk_reset": "",
                "trashtalk_list": "",
                "stats": "(member)",
                "invites": "",
                "info": "(member)",
                "rank": "",
                "trashtalk": "*(mention)*",
                "trashtalk_add": "*(words)*",
                "ping": "",
                "meme": "",
                "font": "*(keyword)* (font)",
                "w2g": "(url)",
                "trump": "",
                "trump_img": "",
                "gen_meme": "(*Top Text*, Bottom Text)",
                "mafia": "*(mention)*",
                "coin": "",
                "auszeit": "*(mention)* *(seconds)*",
                "kick": "(mention)",
                "ban": "*(mention)*",
                "unban": "*(mention)*",
                "invite": "(max_age) (max_uses) (temporary) (unique) (reason)",
                "font_list": "",
                "avatar": "Mention another User to get his Avatar. Nothing if you want your Avatar.",
                "faceit_finder": "Steam URL or ID",
                "set_auto_role": "Mention a Role",
                "google": "(member) (text)",
                "set_welcome_message": "(*message) Available parameters in message: {member} {inviter}"}

    prefix = get_prefix(ctx.guild.id)

    embed = Embed(title="Ungültige Parameter",
                  description=f"Die Werte die du an den Command `{prefix}{command}` übergeben hast sind ungültig.",
                  color=0x1acdee)
    embed.add_field(name=f"Richtigen Parameter:", value=f"`{commands[command]}`", inline=True)

    embed.set_author(name="Zemo Bot", icon_url=ICON_URL)
    await ctx.send(embed=embed)
