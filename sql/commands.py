from general import conn_main, cur_main, decode_data, InvalidGuild


def get_all_guild_commands(guild_id: int):
    cur_main.execute("SELECT CATEGORY_ID, COMMAND FROM COMMANDS WHERE ID NOT IN (SELECT COMMAND_ID FROM DISABLED_COMMANDS WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s))", (guild_id,))
    commands = {command: category for (category, command) in cur_main.fetchall()}

    for command in commands:
        cur_main.execute("SELECT CATEGORY FROM COMMAND_CATEGORIES WHERE ID=%s", (commands[command],))
        commands[command] = cur_main.fetchone()[0]

    return commands
