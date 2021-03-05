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
    cur_main.execute("ALTER TABLE USER_LANGUAGES ADD FOREIGN KEY (user_id) REFERENCES PARTNER_FRIEND (user_id)")
    cur_main.execute("ALTER TABLE USER_INTERESTS ADD FOREIGN KEY (user_id) REFERENCES PARTNER_DATING (user_id)")
    cur_main.execute("ALTER TABLE USER_INTERESTS ADD FOREIGN KEY (user_id) REFERENCES PARTNER_FRIEND (user_id)")
    cur_main.execute("ALTER TABLE USER_INTERESTS ADD FOREIGN KEY (user_id) REFERENCES INTERESTS (interest_id)")
    cur_main.execute("ALTER TABLE USER_LANGUAGES ADD FOREIGN KEY (language_id) REFERENCES LANGUAGES (language_id)")

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


#setup_partner_db()


def insert_gaming(server, user, games, languages, status="initial"):
    sql = "INSERT INTO PARTNER_GAMES (status, server, user) VALUES (%s, %s, %s);"
    val = (str(status), str(server), str(user))

    cur_main.execute(sql, val)
    conn_main.commit()

    cur_main.execute("SELECT LAST_INSERT_ID();")
    user_id = cur_main.fetchone()[0]
    print([(user_id, x) for x in languages])

    cur_main.executemany("INSERT INTO user_games (user_id, game_id) VALUES (%s, %s)", [(user_id, x) for x in games])
    cur_main.executemany("INSERT INTO user_languages (user_id, language_id) VALUES (%s, %s)",
                         [(user_id, x) for x in languages])
    conn_main.commit()


insert_gaming(1231231232, "Ramo#3413", [1, 3, 4], [1, 2, 3])
