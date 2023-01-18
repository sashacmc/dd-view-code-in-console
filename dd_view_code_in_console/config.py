import os
import sys


from configparser import ConfigParser


class Config(object):
    DEFAULTS = {
        "main": {
            "terminal": "konsole",
            "editor": "vim",
        },
        "repositories": {},
    }

    def __init__(self, filename, create=False):
        self.__config = ConfigParser()
        self.__config.read_dict(self.DEFAULTS)
        self.__config.read(filename)

        if create:
            self.__create_if_not_exists(filename)

    def __create_if_not_exists(self, filename):
        if os.path.exists(filename):
            return

        with open(filename, 'w') as conffile:
            self.__config.write(conffile)

    def get_terminal(self):
        return self.__config["main"]["terminal"]

    def get_editor(self):
        return self.__config["main"]["editor"]

    def get_local_path(self, repo):
        return self.__config["repositories"][repo]


if __name__ == "__main__":
    Config(sys.argv[1], create=True)
