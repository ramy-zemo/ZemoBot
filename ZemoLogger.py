import datetime

import inspect


class ZemoLogger:
    def __init__(self, logging_level="", file_name=""):
        self.logging_level = logging_level
        self.file_name = file_name

        if self.file_name:
            file = open(file_name, "w")
            file.close()

    def info(self, info):
        if self.logging_level.lower() != "info" and self.logging_level.lower() != "debug":
            return

        filename = inspect.stack()[1].filename.split("\\")[-1]
        line_number = inspect.currentframe().f_back.f_lineno

        if self.file_name:
            with open(self.file_name, "a+") as file:
                file.write(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " | INFO | " + f"File: {filename}, Line: {line_number} | " + info + " |" + "\n")
        else:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " | INFO | " + f"File: {filename}, Line: {line_number} | " + info + " |" + "\n")

    def warn(self, warning):
        if self.logging_level.lower() != "warn" and self.logging_level.lower() != "debug":
            return

        filename = inspect.stack()[1].filename.split("\\")[-1]
        line_number = inspect.currentframe().f_back.f_lineno

        if self.file_name:
            with open(self.file_name, "a+") as file:
                file.write(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " | WARN | " + f"File: {filename}, Line: {line_number} | " + warning + " |" + "\n")
        else:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " | WARN | " + f"File: {filename}, Line: {line_number} | " + warning + " |" + "\n")

    def error(self, error):
        if self.logging_level.lower() != "error" and self.logging_level.lower() != "debug":
            return

        filename = inspect.stack()[1].filename.split("\\")[-1]
        line_number = inspect.currentframe().f_back.f_lineno

        if self.file_name:
            with open(self.file_name, "a+") as file:
                file.write(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " | ERROR | " + f"File: {filename}, Line: {line_number} | " + error + " |" + "\n")
        else:
            print(datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " | ERROR | " + f"File: {filename}, Line: {line_number} | " + error + " |" + "\n")


