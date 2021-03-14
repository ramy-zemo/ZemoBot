from sql.general import conn_main, cur_main, decode_data, InvalidGuild


def check_command_status_for_guild(guild_id: int, command: str):
    sql = "SELECT ID FROM COMMANDS WHERE COMMAND=%s"
    val = (command,)

    cur_main.execute(sql, val)
    data = cur_main.fetchone()

    if data and data[0]:
        sql_ = "SELECT * FROM DISABLED_COMMANDS WHERE COMMAND_ID=%s AND SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)"
        val_ = (command, guild_id)

        cur_main.execute(sql_, val_)
        data_ = cur_main.fetchone()
        return not data_

    else:
        return False


def disable_command(guild_id: int, command: str):
    cur_main.execute("SELECT ID FROM COMMANDS WHERE COMMAND=%s", (command,))
    command_in_db = cur_main.fetchone()

    if command_in_db:
        sql = "INSERT INTO DISABLED_COMMANDS (SERVER_ID, COMMAND_ID) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s)"
        val = (guild_id, command_in_db[0])

        cur_main.execute(sql, val)
        conn_main.commit()


def enable_command(guild_id: int, command: str):
    if check_command_status_for_guild(guild_id, command):
        return

    sql = "DELETE FROM DISABLED_COMMANDS WHERE COMMAND_ID=(SELECT ID FROM COMMANDS WHERE COMMAND=%s) AND SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)"
    val = (command, guild_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def get_all_disabled_commands_from_guild(guild_id: int) -> list:
    cur_main.execute("SELECT COMMAND_ID FROM DISABLED_COMMANDS WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)", (guild_id,))
    command_ids = cur_main.fetchall()
    data = []

    for command_id in command_ids:
        cur_main.execute("SELECT COMMAND FROM COMMANDS WHERE ID=%s", command_id)
        data.append(cur_main.fetchone()[0])

    return data
