import sqlite3

def effify(non_f_str: str):
    return eval(f'f"""{non_f_str}"""')

conn_main = sqlite3.connect("main.db")
cur_main = conn_main.cursor()

cur_main.execute(f"DELETE FROM TrashTalk WHERE server=? AND von=?", (str(481248489238429727), str("Ramo#4907")))
conn_main.commit()