from general import conn_main, cur_main, decode_data, InvalidGuild


def insert_user_xp(guild_id: int, user_id: int, xp: int):
    sql = "INSERT INTO LEVEL (SERVER_ID, USER_ID, XP) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s)"
    val_1 = (guild_id, user_id, xp)

    try:
        cur_main.execute(sql, val_1)
        conn_main.commit()
    except mysql.connector.errors.IntegrityError:
        raise InvalidGuild


def get_xp_from_user(guild_id: int, user_id: int) -> int:
    cur_main.execute("SELECT SUM(XP) FROM LEVEL WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND USER_ID=%s", (guild_id, user_id))
    data = cur_main.fetchone()

    return data[0] if data and data[0] else 0


def get_server_ranks(guild_id: int) -> list:
    sql = "SELECT * FROM LEVEL WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) ORDER BY XP ASC"
    val = (guild_id,)

    cur_main.execute(sql, val)
    data = cur_main.fetchall()

    new = {}
    done_users = []

    for entry in decode_data(data):
        if entry[1] in done_users:
            continue

        for second in decode_data(data):
            if second[0] == entry[0] and second[1] == entry[1]:
                if second[1] in new:
                    new[second[1]] += second[2]
                else:
                    new[second[1]] = second[2]

        done_users.append(entry[1])

    return [(k, v) for k, v in new.items()]


def update_user_xp(guild_id: int, user_id: int, xp: int):
    cur_main.execute("DELETE FROM LEVEL WHERE SERVER_ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s) AND USER_ID=%s", (guild_id, user_id))
    conn_main.commit()

    sql = "INSERT INTO LEVEL (SERVER_ID, USER_ID, XP) VALUES ((SELECT ID FROM CONFIG WHERE GUILD_ID=%s), %s, %s)"
    val = (guild_id, user_id, xp)

    cur_main.execute(sql, val)
    conn_main.commit()
