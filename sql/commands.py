from sql.general import conn_main, cur_main, decode_data, InvalidGuild


def get_all_guild_commands(guild_id: int):
    cur_main.execute("SELECT CATEGORY_ID, COMMAND FROM COMMANDS WHERE ID NOT IN (SELECT COMMAND_ID FROM DISABLED_COMMANDS WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s))", (guild_id,))
    commands = {command: category for (category, command) in cur_main.fetchall()}

    for command in commands:
        cur_main.execute("SELECT CATEGORY FROM COMMAND_CATEGORIES WHERE ID=%s", (commands[command],))
        commands[command] = cur_main.fetchone()[0]
    return commands


def get_all_guild_commands_from_category(guild_id: int, category: str):
    cur_main.execute("SELECT COMMAND, PARAMETERS, DESCRIPTION FROM COMMANDS WHERE ID NOT IN (SELECT COMMAND_ID FROM DISABLED_COMMANDS WHERE ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)) AND CATEGORY_ID=(SELECT ID FROM COMMAND_CATEGORIES WHERE CATEGORY=%s)", (guild_id, category))
    return cur_main.fetchall()


def create_command(category: str, command: str, parameters: str, description: str):
    sql = "INSERT INTO COMMANDS (CATEGORY_ID, COMMAND, PARAMETERS, DESCRIPTION) VALUES ((SELECT ID FROM COMMAND_CATEGORIES WHERE CATEGORY=%s), %s, %s, %s)"
    val = (category, command, parameters, description)

    cur_main.execute(sql, val)
    conn_main.commit()


def delete_command(command: str):
    sql = "DELETE FROM COMMANDS WHERE COMMAND=%s"
    val = (command,)

    cur_main.execute(sql, val)
    conn_main.commit()
