from sql.general import conn_main, cur_main, decode_data, InvalidGuild


def get_all_admin_commands():
    cur_main.execute("SELECT COMMAND FROM ADMIN_COMMANDS")
    return [commands[0] for commands in cur_main.fetchall()]


def create_admin_command(command: str, parameters: str, description: str):
    sql = "INSERT INTO ADMIN_COMMANDS (COMMAND, PARAMAETERS, DESCRIPTION) VALUES (%s, %s, %s)"
    val = (command, parameters, description)

    cur_main.execute(sql, val)
    conn_main.commit()


def delete_admin_command(command: str):
    sql = "DELETE FROM ADMIN_COMMANDS WHERE COMMAND=%s"
    val = (command,)

    cur_main.execute(sql, val)
    conn_main.commit()
