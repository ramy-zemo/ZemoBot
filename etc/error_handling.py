from discord import Embed


async def invalid_argument(ctx, command, usage):
    embed = Embed(title="Ungültige Parameter",
                          description=f"Die Werte die du an den Command `${command}` übergeben hast sind ungültig.",
                          color=0x1acdee)
    embed.add_field(name=f"Richtigen Parameter:", value=f"`{usage}`", inline=True)

    embed.set_author(name="Zemo Bot", icon_url="https://www.zemodesign.at/wp-content/uploads/2020/05/Favicon-BL-BG.png")
    await ctx.send(embed=embed)
