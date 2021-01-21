from discord import Embed


async def invalid_argument(ctx, command):
    commands = {"trashtalk_stats": "$trashtalk_stats (member)",
                "trashtalk_reset": "",
                "trashtalk_list": "",
                "stats": "(member)",
                "invites": "",
                "info": "(member)",
                "rank": "",
                "trashtalk": "**(mention)**",
                "trashtalk_add": "**(words)**",
                "ping": "",
                "meme": "",
                "font": "**(keyword)** (font)",
                "w2g": "(url)",
                "trump": "",
                "trump_img": "",
                "gen_meme": "(**Top Text**, Bottom Text)",
                "mafia": "**(mention)**",
                "coin": "",
                "auszeit": "**(mention)** **(seconds)**",
                "kick": "(mention)",
                "ban": "**(mention)**",
                "unban": "**(mention)**",
                "invite": "(max_age) (max_uses) (temporary) (unique) (reason)",
                "font_list": "",
                "avatar (mention)": "Get the Discord Avatar from a user.",
                "faceit_finder **(steam_url)**": "Find a FaceIt account by Steam identifier."}

    embed = Embed(title="Ungültige Parameter",
                  description=f"Die Werte die du an den Command `${command}` übergeben hast sind ungültig.",
                  color=0x1acdee)
    embed.add_field(name=f"Richtigen Parameter:", value=f"`{commands[command]}`", inline=True)

    embed.set_author(name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
    await ctx.send(embed=embed)



