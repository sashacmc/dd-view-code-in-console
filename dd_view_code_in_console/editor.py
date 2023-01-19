import sys


class BaseEditor(object):
    def get_command(self, file, line, column):
        pass


class VimEditor(BaseEditor):
    def get_command(self, file, line, column):
        if line is None:
            return f"vim {file}"
        if column is None:
            return f"vim -c {line} {file}"
        return f"vim '+normal {line}G{column}|' {file}"


class NanoEditor(BaseEditor):
    def get_command(self, file, line, column):
        if line is None:
            return f"nano {file}"
        if column is None:
            return f"nano +{line} {file}"
        return f"nano +{line},{column} {file}"


class EmacsEditor(BaseEditor):
    def get_command(self, file, line, column):
        if line is None:
            return f"emacs {file}"
        if column is None:
            return f"emacs +{line} {file}"
        return f"emacs +{line}:{column} {file}"


EDITORS = {
    "vim": VimEditor,
    "nano": NanoEditor,
    "emacs": EmacsEditor,
}


def get_editor(name):
    if name in EDITORS:
        return EDITORS[name]()
    else:
        raise Exception(f"Unknown editor {name}")
