from dotenv import load_dotenv
import mysql.connector

load_dotenv()

DB_IP = "ni215803-1.web10.nitrado.hosting"
DB_USER = "ni215803_1sql1"
DB_PASSWORD = "3b73aafc"
DB_DATABASE = "ni215803_1sql1"

conn_main = mysql.connector.connect(
    host=DB_IP,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_DATABASE,
    auth_plugin='mysql_native_password'
)
cur_main = conn_main.cursor()

cur_main.execute("""CREATE TABLE IF NOT EXISTS `LANGUAGES`(
`ID`       INT PRIMARY KEY AUTO_INCREMENT,
`LANGUAGE` TEXT);
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `CONFIG`(
`ID`                 INT PRIMARY KEY AUTO_INCREMENT,
`ACTIVE`             boolean,
`GUILD_ID`           BIGINT,
`LANGUAGE`            INT,
`PREFIX`             TEXT,
`MESSAGE_CHANNEL_ID` BIGINT,
`WELCOME_CHANNEL_ID` BIGINT,
`WELCOME_MESSAGE`    TEXT,
`WELCOME_ROLE_ID`    BIGINT,
`TWITCH_USERNAME`    TEXT,
CONSTRAINT `CONFIG_LANGUAGE_LANGUAGES` FOREIGN KEY (LANGUAGE) REFERENCES LANGUAGES (ID));
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `INVITES`(
`SERVER_ID`           INT not null,
`DATE`         DATE,
`FROM_USER_ID` BIGINT,
`TO_USER_ID`   BIGINT,
CONSTRAINT `INVITE_CONFIG` FOREIGN KEY (SERVER_ID) REFERENCES CONFIG (ID));
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `LEVEL`(
`SERVER_ID`      INT not null,
`USER_ID` BIGINT,
`XP`      BIGINT,
CONSTRAINT `LEVEL_CONFIG` FOREIGN KEY (SERVER_ID) REFERENCES CONFIG (ID));
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `MESSAGE`(
`SERVER_ID`      INT not null,
`DATE`    DATE,
`USER_ID` BIGINT,
`MESSAGE` TEXT,
CONSTRAINT `MESSAGE_CONFIG` FOREIGN KEY (SERVER_ID) REFERENCES CONFIG (ID));
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `TRASHTALK`(
`SERVER_ID`               INT not null,
`ADDED_ON`         DATE,
`ADDED_BY_USER_ID` BIGINT,
`MESSAGE`          TEXT,
CONSTRAINT `TRASHTALK_CONFIG` FOREIGN KEY (SERVER_ID) REFERENCES CONFIG (ID));
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `TRASHTALK_LOG`(
`SERVER_ID`           INT not null,
`DATE`         DATE,
`FROM_USER_ID` BIGINT,
`TO_USER_ID`   BIGINT,
CONSTRAINT `TRASHTALK_LOG_CONFIG` FOREIGN KEY (SERVER_ID) REFERENCES CONFIG (ID));
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `VOICE`(
`SERVER_ID`      INT not null,
`USER_ID` BIGINT,
`MINUTES` BIGINT,
CONSTRAINT `VOICE_CONFIG` FOREIGN KEY (SERVER_ID) REFERENCES CONFIG (ID));
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `COMMAND_CATEGORIES`(
`ID`       INT PRIMARY KEY AUTO_INCREMENT,
`CATEGORY` TEXT);
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `COMMANDS`(
`ID`          INT PRIMARY KEY AUTO_INCREMENT,
`CATEGORY_ID`    INT NOT NULL,
`COMMAND`     TEXT,
`PARAMETERS`  TEXT,
`DESCRIPTION` TEXT,
CONSTRAINT `COMMANDS_COMMAND_CATEGORIES` FOREIGN KEY (CATEGORY_ID) REFERENCES COMMAND_CATEGORIES (ID));
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `DISABLED_COMMANDS`(
`SERVER_ID`         INT not null,
`COMMAND_ID` INT,
CONSTRAINT `DISABLED_COMMANDS_COMMANDS` FOREIGN KEY (COMMAND_ID) REFERENCES COMMANDS (ID),
CONSTRAINT `DISABLED_COMMANDS_CONFIG` FOREIGN KEY (SERVER_ID) REFERENCES CONFIG (ID));
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `ADMIN_COMMANDS` (
`ADMIN_COMMAND_ID` INT PRIMARY KEY AUTO_INCREMENT,
`COMMAND` TEXT,
`PARAMETERS` TEXT,
`DESCRIPTION` TEXT);
""")

cur_main.execute("""CREATE TABLE IF NOT EXISTS `COMMAND_ALIASES`(
`COMMAND_ID` INT not null,
`ALIAS` TEXT,
CONSTRAINT `COMMAND_ALIASES_COMMANDS` FOREIGN KEY (COMMAND_ID) REFERENCES COMMANDS (ID));
""")

conn_main.commit()

# COMMAND_CATEGORIES
command_categories = [("level",),
                      ("fun",),
                      ("games",),
                      ("mod",),
                      ("media",),
                      ("search",),
                      ("config",)]

cur_main.executemany("INSERT INTO COMMAND_CATEGORIES (CATEGORY) VALUES (%s)", command_categories)
conn_main.commit()

commands = [(2, "trashtalk", "(*mention)", "Spam users with terms defined on your server."),
            (1, "trashtalk_stats", "", "Show your Trashtalk statistics."),
            (1, "trashtalk_reset", "", "Reset your Trashtalk statistics."),
            (1, "trashtalk_list", "", "Show Trashtalk terms defined on your server."),
            (2, "trashtalk_add", "", "Add terms to your Trashtalk list."),
            (3, "mafia", "(*mention)", "Start Mafia Game."),
            (2, "ping", "", "Get the bot latency."),
            (1, "stats", "(mention)", "Get your Server statistics."),
            (4, "auszeit", "(*mention) (*seconds)", "Timeout Users."),
            (2, "meme", "", "Get a random meme from Reddit."),
            (2, "font", "(*keyword) (font)", "Get ASCII Art from provided keyword."),
            (5, "font_list", "", "Get List of available Fonts."),
            (4, "create_invite", "(max_age) (max_uses) (temporary) (unique) (reason)", "Create server invites."),
            (2, "w2g", "(url)", "Create watch2gether room with provided Link."),
            (1, "info", "(mention)", "Get your user information."),
            (2, "trump", "", "Get a random quote of Trump."),
            (2, "trump_img", "", "Get a random picture of a Trump meme."),
            (2, "gen_meme", "(*Top Text) (Bottom Text)", "Get a custom Meme."),
            (5, "avatar", "(mention)", "Get a Discord profile picture."),
            (4, "invite_bot", "", "Get an invitation to invite the bot to another server."),
            (4, "ban", "(*mention)", "Ban Members."),
            (4, "kick", "(*mention)", "Kick Members."),
            (4, "unban", "(*mention)", "Unban Members."),
            (6, "faceit_finder", "(steam_url)", "Find a FaceIt account using the Steam Profile URL."),
            (7, "set_auto_role", "(*mention_role)",
             "Determine the role that each new member will automatically receive."),
            (6, "google", "(mention) (*text)",
             "Creates a Google it Yourself link and shortens it when the Shortener API is available."),
            (7, "set_prefix", "(*prefix)", "Determine the bot prefix on your server."),
            (7, "enable_command", "(*command)", "Enable the use of a specific command on your server."),
            (7, "disable_command", "(*command)", "Disable the use of a specific command on your server."),
            (1, "invites", "", "List of your successful invitations."),
            (5, "server_info", "", "Get some Server statistics."),
            (3, "coin", "", "Flip a ZEMO Coin."),
            (3, "pick_number", "(minimum) (maximum)", "Pick a random number from a certain range."),
            (1, "ranking", "", "List of the top 5 server ranks."),
            (7, "setup_twitch", "(*username)", "Connect a Twitch username to the server."),
            (7, "set_welcome_message", "(*message)",
             "Set a welcome message for new members. Available parameters in the message: {member} {inviter}"),
            (7, "help", "(category)", "Get a list of available commands."),
            (5, "ripple", "", "Get current Ripple rate."),
            (5, "bitcoin", "", "Get current Bitcoin rate."),
            (5, "ethereum", "", "Get current Ethereum rate.")
            ]

admin_commands = [("show_channels", "", "Print all available channels on your Guild."),
                  ("show_roles", "", "Print all available roles on your Guild."),
                  ("set_xp", "(mention) (xp)", "Set the Xp of a user"),
                  ("partner", "", ""),
                  ("add_command", "(*category) (*command) (*parameters) (*description)", "Add command to ZemoBot."),
                  ("add_admin_command", "(*category) (*command) (*parameters) (*description)",
                   "Add Admin command to ZemoBot."),
                  ("delete_command", "(*command)", "Remove command from ZemoBot."),
                  ("delete_admin_command", "(*command)", "Remove Admin command from ZemoBot.")
                  ]

languages = [("german",),
             ("english",),
             ("russian",)]

command_aliases = [(14, "watch2gether")]

cur_main.executemany("INSERT INTO COMMANDS (CATEGORY_ID, COMMAND, PARAMETERS, DESCRIPTION) VALUES (%s, %s, %s, %s)",
                     commands)
cur_main.executemany("INSERT INTO ADMIN_COMMANDS (COMMAND, PARAMETERS, DESCRIPTION) VALUES (%s, %s, %s)",
                     admin_commands)

cur_main.executemany("INSERT INTO LANGUAGES (LANGUAGE) VALUES (%s)", languages)

cur_main.executemany("INSERT INTO COMMAND_ALIASES (command_id, alias) VALUES (%s, %s)", command_aliases)

conn_main.commit()