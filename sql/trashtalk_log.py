from general import conn_main, cur_main, decode_data, InvalidGuild


def get_user_trashtalk(guild_id: int, user_id: int) -> list:
    sql = "SELECT * FROM TRASHTALK_LOG WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND FROM_USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()
    return decode_data(data)


def reset_trashtalk(guild_id: int, user_id: int):
    sql = "DELETE FROM TRASHTALK_LOG WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND FROM_USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def log_trashtalk(guild_id: int, datum: str, from_user_id: int, to_user_id: int):
    sql = "INSERT INTO TRASHTALK_LOG (SERVER_ID, DATE, FROM_USER_ID, TO_USER_ID) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, datum, from_user_id, to_user_id)

    cur_main.execute(sql, val)
    conn_main.commit()
