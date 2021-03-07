from sql.general import conn_main, cur_main, decode_data, InvalidGuild


def get_trashtalk(guild_id: int) -> list:
    sql = "SELECT MESSAGE FROM TRASHTALK WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)"
    val = (guild_id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()

    return [x[0] for x in decode_data(data) if x[0]]


def add_trashtalk(guild_id: int, added_on: str, added_by_user_id: int, message: str):
    sql = "INSERT INTO TRASHTALK (SERVER_ID, ADDED_ON, ADDED_BY_USER_ID, MESSAGE) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, added_on, added_by_user_id, message)

    cur_main.execute(sql, val)
    conn_main.commit()
