import sys


class BaseEditor(object):
    def get_command(self, file, line, column):
        pass


class VimEditor(BaseEditor):
    def get_command(self, file, line, column):
        return f"vim '+normal {line}G{column}|' {file}"


class NanoEditor(BaseEditor):
    def get_command(self, file, line, column):
        pass


EDITORS = {
    "vim": VimEditor,
    "nano": NanoEditor,
}


def get_editor(name):
    if name in EDITORS:
        return EDITORS[name]()
    else:
        raise Exception(f"Unknown editor {name}")
