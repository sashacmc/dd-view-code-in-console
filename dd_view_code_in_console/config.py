class Config(object):
    def __init__(self, filename):
        pass

    def get_terminal(self):
        return "iterm2"

    def get_editor(self):
        return "vim"

    def get_local_path(self, repo):
        return "~/dd/dd-go/"
