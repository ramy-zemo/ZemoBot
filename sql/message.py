from general import conn_main, cur_main, decode_data, InvalidGuild


def get_user_messages(user_id: int) -> list:
    cur_main.execute("SELECT * from MESSAGE WHERE USER_ID=%s", (user_id,))
    data = cur_main.fetchall()
    return decode_data(data)


def log_message(guild_id: int, date: str, user_id: int, message: str):
    sql = "INSERT INTO MESSAGE (SERVER_ID, DATE, USER_ID, MESSAGE) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, date, user_id, message)

    cur_main.execute(sql, val)
    conn_main.commit()
