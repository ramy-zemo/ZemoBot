import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

conn_main = mysql.connector.connect(
    host=os.getenv('db_ip'),
    user=os.getenv('db_user'),
    password=os.getenv('db_password'),
    database="Partner"
)
cur_main = conn_main.cursor()


def setup_partner_db():
    # Creations
    cur_main.execute("CREATE TABLE IF NOT EXISTS PARTNER_GAMES (user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                     "status TEXT, server TEXT, user TEXT)")

    cur_main.execute("CREATE TABLE IF NOT EXISTS PARTNER_DATING (user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                     "status TEXT, server TEXT, user TEXT, gender TEXT, age TEXT, sexuality TEXT,"
                     "region TEXT )")

    cur_main.execute("CREATE TABLE IF NOT EXISTS PARTNER_FRIEND (user_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                     "status TEXT, server TEXT, user TEXT, age TEXT )")

    cur_main.execute("CREATE TABLE IF NOT EXISTS USER_GAMES (user_id INT, game_id INT );")
    cur_main.execute("CREATE TABLE IF NOT EXISTS USER_LANGUAGES (user_id INT, language_id INT )")
    cur_main.execute("CREATE TABLE IF NOT EXISTS USER_INTERESTS (user_id INT, interest_id INT )")

    cur_main.execute("CREATE TABLE IF NOT EXISTS INTERESTS (interest_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                     "interest TEXT )")

    cur_main.execute("CREATE TABLE IF NOT EXISTS LANGUAGES (language_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
                     "language TEXT )")

    cur_main.execute("CREATE TABLE IF NOT EXISTS GAMES (game_id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, game TEXT )")

    # References
    cur_main.execute("ALTER TABLE USER_GAMES ADD FOREIGN KEY (user_id) REFERENCES PARTNER_GAMES (user_id)")
    cur_main.execute("ALTER TABLE USER_LANGUAGES ADD FOREIGN KEY (user_id) REFERENCES PARTNER_GAMES (user_id)")
    cur_main.execute("ALTER TABLE USER_GAMES ADD FOREIGN KEY (game_id) REFERENCES GAMES (game_id)")
    cur_main.execute("ALTER TABLE USER_LANGUAGES ADD FOREIGN KEY (language_id) REFERENCES INTERESTS (interest_id)")
    cur_main.execute("ALTER TABLE USER_LANGUAGES ADD FOREIGN KEY (user_id) REFERENCES PARTNER_FRIEND (user_id)")
    cur_main.execute("ALTER TABLE USER_INTERESTS ADD FOREIGN KEY (user_id) REFERENCES PARTNER_DATING (user_id)")
    cur_main.execute("ALTER TABLE USER_INTERESTS ADD FOREIGN KEY (interest_id) REFERENCES LANGUAGES (language_id)")
    cur_main.execute("ALTER TABLE USER_INTERESTS ADD FOREIGN KEY (user_id) REFERENCES PARTNER_FRIEND (user_id)")

    # Insertions
    available_languages = [('chinese',), ('spanish',), ('english',), ('hindi',), ('arabic',), ('russian',), ('german',),
                           ('french',), ('bosnian / serbian / croatian',), ('hungarian',)]

    cur_main.executemany("INSERT INTO LANGUAGES (language) VALUE (%s)", available_languages)

    available_games = [('league of legends',), ('among us',), ('apex legends',), ('fortnite',),
                       ("playerunknown's battlegrounds",), ("tom clancy's rainbow six siege",),
                       ('counter-strike: global offensive',), ('minecraft',), ('call of duty',), ('grand theft auto',)]

    cur_main.executemany("INSERT INTO GAMES (game) VALUE (%s)", available_games)

    available_interests = [('swimming',), ('cooking',), ('gaming',), ('sports',), ('listening to music',),
                           ('playing soccer',), ('reading',), ('programming',), ('traveling',), ('photographing',)]

    cur_main.executemany("INSERT INTO INTERESTS (interest) VALUE (%s)", available_interests)

    conn_main.commit()


setup_partner_db()
