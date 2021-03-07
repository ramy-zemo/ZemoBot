from sql.general import conn_main, cur_main, decode_data


def get_all_guild_categories(guild_id: int):
    cur_main.execute("SELECT CATEGORY FROM COMMAND_CATEGORIES WHERE ID IN (SELECT CATEGORY_ID FROM COMMANDS WHERE ID NOT IN (SELECT COMMAND_ID FROM DISABLED_COMMANDS WHERE ID=(SELECT ID FROM CONFIG WHERE GUILD_ID=%s)))", (guild_id,))

    return [x[0] for x in cur_main.fetchall() if x[0]]

