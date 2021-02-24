CREATE TABLE IF NOT EXISTS `CONFIG` ( `ID` INT PRIMARY KEY AUTO_INCREMENT, `ACTIVE` boolean, `GUILD_ID` INT, `SPRACHE` TEXT, `PREFIX` TEXT, `MESSAGE_CHANNEL_ID` INT, `WELCOME_CHANNEL_ID` INT, `WELCOME_MESSAGE` TEXT, `WELCOME_ROLE_ID` INT, `TWITCH_USERNAME` TEXT);
CREATE TABLE IF NOT EXISTS `INVITES` ( `ID` INT, `DATE` DATE, `FROM_USER_ID` INT, `TO_USER_ID` INT, CONSTRAINT `INVITE_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));
CREATE TABLE IF NOT EXISTS `LEVEL` ( `ID` INT, `USER_ID` INT, `XP` INT, CONSTRAINT `LEVEL_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));
CREATE TABLE IF NOT EXISTS `MESSAGE` ( `ID` INT, `DATE` DATE, `USER_ID` INT, `MESSAGE` TEXT, CONSTRAINT `MESSAGE_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));
CREATE TABLE IF NOT EXISTS `TRASHTALK` ( `ID` INT, `DATE` DATE, `FROM_USER_ID` INT, `TO_USER_ID` INT, CONSTRAINT `TRASHTALK_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));
CREATE TABLE IF NOT EXISTS `VOICE` ( `ID` INT, `USER_ID` INT, `minutes` INT, CONSTRAINT `VOICE_SERVER` FOREIGN KEY (ID) REFERENCES CONFIG (ID));
CREATE TABLE IF NOT EXISTS `COMMANDS` ( `ID` INT PRIMARY KEY AUTO_INCREMENT, `COMMAND` TEXT, `PARAMETERS` TEXT, `DESCRIPTION` TEXT);
CREATE TABLE IF NOT EXISTS `DISABLED_COMMANDS` ( `ID` INT, `COMMAND_ID` INT, CONSTRAINT `DISABLED_COMMANDS_COMMANDS` FOREIGN KEY (ID) REFERENCES CONFIG (ID), CONSTRAINT `DISABLED_COMMANDS_COMMANDS` FOREIGN KEY (COMMAND_ID) REFERENCES COMMANDS (ID));