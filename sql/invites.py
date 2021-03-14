from sql.general import conn_main, cur_main, decode_data, InvalidGuild


def log_invite(guild_id: int, date: str, from_user_id: int, to_user_id: int):
    sql = "INSERT INTO INVITES (SERVER_ID, DATE, FROM_USER_ID, TO_USER_ID) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s, %s)"
    val = (guild_id, date, from_user_id, to_user_id)

    cur_main.execute(sql, val)
    conn_main.commit()


def get_invites_to_user(guild_id: int, invite_to_user_id: int) -> list:
    sql = "SELECT * FROM INVITES WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND TO_USER_ID=%s"
    val = (guild_id, invite_to_user_id)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()
    return decode_data(data)


async def get_user_invites(guild_id: int, user_id: int) -> list:
    sql = "SELECT * FROM INVITES WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND FROM_USER_ID=%s"
    val = (guild_id, user_id)

    cur_main.execute(sql, val)
    invites = cur_main.fetchall()
    return invites