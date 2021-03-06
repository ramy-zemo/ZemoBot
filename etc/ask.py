import asyncio
import discord

from config import ICON_URL


async def ask_for_thumbs(bot, ctx, title, question):
    embed = discord.Embed(title=title, description=question, color=0x1acdee)

    embed.set_author(name="Zemo Bot", icon_url=ICON_URL)
    embed.set_footer(text="Reagiere auf diese Nachricht um diese Frage zu beantworten.")

    request = await ctx.send(embed=embed)

    for emoji in ('👍', '👎'):
        await request.add_reaction(emoji)

    def check(reaction, author):
        return str(reaction.emoji) in ['👍', '👎'] and str(author) != str(bot.user) and str(author) == str(
            ctx.message.author)

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)

    except asyncio.TimeoutError:
        await ctx.send("Deine Antwort hat zu lange gedauert.")
        return False

    return reaction.emoji == '👍'


async def ask(author, ask_type, question, text_channel, bot, options=0, max_answers=9999, range_int=[0, 100],
              msg_type="text", reaction_type="usual", msg_max_length=0, msg_description=""):
    class InvalidInt(Exception):
        pass

    class TooMuchReaction(Exception):
        pass

    class TooLongReaction(Exception):
        pass

    sent_messages = []
    while True:
        if options:
            embed = discord.Embed(title=question, description='\n'.join(options), color=0x1acdee)
        else:
            embed = discord.Embed(title=question, description=msg_description, color=0x1acdee)

        if ask_type == "reaction_add" and reaction_type == "bool":
            embed.description = "1. Ja\n2. Nein"

        embed.set_author(name="Zemo Bot", icon_url=ICON_URL)
        embed.set_footer(text=f"Reagiere auf diese Nachricht um eine Auswahl zu treffen. Maximale Auswahlmöglichkeiten: {max_answers}")

        request = await text_channel.send(embed=embed)
        sent_messages.append(request)
        emojis = {1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣", 6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"}

        if ask_type == "reaction_add":
            if not options:
                for count in range(2):
                    await request.add_reaction(emojis[count + 1])
                else:
                    await request.add_reaction("⏭")
            else:
                for count in range(len(options)):
                    await request.add_reaction(emojis[count + 1])
                else:
                    await request.add_reaction("⏭")

        reactions = []

        def reaction_add(reaction, user):
            if reaction.message.channel != text_channel:
                return
            if str(user) == str(bot.user):
                return False
            if str(user) != author and reaction.emoji != "⏭":
                reactions.append(reaction)

            if str(reaction.emoji) in ["⏭"]:
                if len(reactions) > max_answers:
                    raise TooMuchReaction
                return True

        def check_message(reaction):
            if reaction.channel != text_channel or str(reaction.author) == str(bot.user):
                return

            if msg_type == "int":
                if range_int != [0, 100]:
                    try:
                        if range_int[0] < int(reaction.content) < range_int[1]:
                            return True
                        elif int(reaction.content) < range_int[0]:
                            raise InvalidInt
                        elif int(reaction.content) > range_int[1]:
                            raise InvalidInt

                    except ValueError:
                        raise InvalidInt
                else:
                    try:
                        int(reaction.content)
                    except ValueError:
                        raise InvalidInt
            elif msg_max_length:
                if len(reaction.content) == msg_max_length:
                    return True
                else:
                    raise TooLongReaction
            else:
                return True

        try:
            check_methods = {"reaction_add": reaction_add, "message": check_message}
            reaction = await bot.wait_for(ask_type, check=check_methods[ask_type])

        except TooMuchReaction:
            embed = discord.Embed(title="Zu viele Optionen gewählt",
                                  description=f"Du hast zu viele Optionen gewählt. Wähle maximal {max_answers}",
                                  color=0x1acdee)
            embed.set_author(name="Zemo Bot", icon_url=ICON_URL)
            embed.set_footer(text=f"Reagiere auf die nächste Nachricht um eine Auswahl zu treffen. Maximale Auswahlmöglichkeiten: {max_answers}")
            sent_messages.append(await text_channel.send(embed=embed))
            continue

        except InvalidInt:
            embed = discord.Embed(title="Ungültige Auswahl", description=f"Die eingegebene Zahl ist nicht gültig.",
                                  color=0x1acdee)
            embed.set_author(name="Zemo Bot", icon_url=ICON_URL)
            embed.set_footer(text=f"Die Auswahl muss zwischen {range_int[0]} und {range_int[1]} liegen.")
            sent_messages.append(await text_channel.send(embed=embed))
            continue

        except TooLongReaction:
            embed = discord.Embed(title="Ungültige Auswahl", description=f"Deine Antwort ist nicht gültig.",
                                  color=0x1acdee)
            embed.set_author(name="Zemo Bot", icon_url=ICON_URL)
            embed.set_footer(text=f"Die Antwort darf maximal {msg_max_length} Zeichen lang sein.")
            sent_messages.append(await text_channel.send(embed=embed))
            continue

        # Delete sent messages
        for msg in sent_messages:
            await msg.delete()
        await text_channel.send("Vielen Dank für die Antwort.")

        answers = []

        if ask_type == "reaction_add":
            for answer in [x.emoji for x in reactions]:
                for count, emoji in enumerate(emojis):
                    if answer == emojis[emoji]:
                        answers.append(count + 1)

        if ask_type == "reaction_add" and reaction_type == "bool":
            answers = answers[0] == 1

        elif ask_type == "message":
            return reaction.content

        return answers
