import mysql.connector

from dotenv import load_dotenv
from config import DB_IP, DB_USER, DB_PASSWORD, DB_DATABASE


load_dotenv()

conn_main = mysql.connector.connect(
    host=DB_IP,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE
)
cur_main = conn_main.cursor()


class InvalidGuild(Exception):
    pass


def decode_data(data) -> list:
    new_data = list()
    for data_set in data:
        entry = list()
        for item in data_set:
            if isinstance(item, bytes):
                entry.append(item.decode())
            else:
                entry.append(item)
        new_data.append(entry)
    return new_data
