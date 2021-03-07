from sql.general import conn_main, cur_main, decode_data, InvalidGuild


def get_user_voice_time(user_id: int) -> int:
    cur_main.execute("SELECT SUM(MINUTES) from VOICE WHERE USER_ID=%s", (user_id,))
    data = cur_main.fetchone()
    return data[0] if data and data[0] else 0


def add_user_voice_time(guild_id: int, user_id: int, minutes: int):
    sql = "INSERT INTO VOICE (SERVER_ID, USER_ID, MINUTES) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s)"
    val = (guild_id, user_id, minutes)

    cur_main.execute(sql, val)
    conn_main.commit()