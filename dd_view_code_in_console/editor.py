import sys


class BaseEditor(object):
    def get_command(self, file, line, column):
        pass


class VimEditor(BaseEditor):
    def get_command(self, file, line, column):
        if line is not None:
            if column is not None:
                return f"vim '+normal {line}G{column}|' {file}"
            else:
                return f"vim -c {line} {file}"
        else:
            return f"vim {file}"


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
