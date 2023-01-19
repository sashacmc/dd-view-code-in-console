import os
import sys
import subprocess


class BaseTerminal(object):
    def open(self, editor, repo, location):
        pass

    def _get_command(self, editor, gitfile):
        return editor.get_command(gitfile.filename(), gitfile.line(), gitfile.column())


class NoneTerminal(BaseTerminal):
    def open(self, editor, gitfile):
        cmd = self._get_command(editor, gitfile)
        subprocess.run(cmd, shell=True)


class ITerm2Terminal(BaseTerminal):
    def open(self, editor, gitfile):
        import iterm2
        import AppKit

        cmd = self._get_command(editor, gitfile)
        command = f'/bin/bash -l -c "{cmd}"'

        AppKit.NSWorkspace.sharedWorkspace().launchApplication_("iTerm.app")

        async def main(connection):
            app = await iterm2.async_get_app(connection)
            window = await iterm2.Window.async_create(connection, command=command)
            await app.async_activate()

        iterm2.run_until_complete(main, True)


class KonsoleTerminal(BaseTerminal):
    def open(self, editor, gitfile):
        cmd = self._get_command(editor, gitfile)
        subprocess.run(("/usr/bin/konsole", "-e", cmd))


class GnomeTerminal(BaseTerminal):
    def open(self, editor, gitfile):
        cmd = self._get_command(editor, gitfile)
        subprocess.run(f"/usr/bin/gnome-terminal --wait -- {cmd}", shell=True)


TERMINALS = {
    "none": NoneTerminal,
    "iterm2": ITerm2Terminal,
    "konsole": KonsoleTerminal,
    "gnome-terminal": GnomeTerminal,
}


def get_terminal(name):
    if name in TERMINALS:
        return TERMINALS[name]()
    else:
        raise Exception(f"Unknown terminal {name}")
