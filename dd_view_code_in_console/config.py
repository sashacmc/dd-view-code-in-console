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
        self.__filename = filename
        self.__config = ConfigParser(delimiters=('=',))
        self.__config.read_dict(self.DEFAULTS)
        self.__config.read(filename)

        if create:
            self.__create_if_not_exists()

    def __create_if_not_exists(self):
        if os.path.exists(self.__filename):
            return

        self.__write()

    def __write(self):
        with open(self.__filename, 'w') as conffile:
            self.__config.write(conffile)

    def add_repositories(self, repositories):
        for url, path in repositories:
            self.__config["repositories"][url] = path
        self.__write()

    def get_terminal(self):
        return self.__config["main"]["terminal"]

    def get_editor(self):
        return self.__config["main"]["editor"]

    def get_local_path(self, repo):
        try:
            return self.__config["repositories"][repo]
        except KeyError:
            print(f"Repository {repo} not configured")
            return ""


if __name__ == "__main__":
    Config(sys.argv[1], create=True)
