import sys
import os


class BaseTerminal(object):
    def open(self, editor, repo, location):
        pass

    def _get_command(self, editor, repo, location):
        return editor.get_command(
            os.path.join(repo, location["path"]), location["line"], location["column"]
        )


class ITerm2Terminal(BaseTerminal):
    def open(self, editor, repo, location):
        import iterm2
        import AppKit

        cmd = self._get_command(editor, repo, location)
        command = f'/bin/bash -l -c "{cmd}"'

        AppKit.NSWorkspace.sharedWorkspace().launchApplication_("iTerm.app")

        async def main(connection):
            app = await iterm2.async_get_app(connection)
            window = await iterm2.Window.async_create(connection, command=command)
            await app.async_activate()

        iterm2.run_until_complete(main, True)


class KonsoleTerminal(BaseTerminal):
    def open(self, editor, repo, location):
        pass


TERMINALS = {
    "iterm2": ITerm2Terminal,
    "konsoile": KonsoleTerminal,
}


def get_terminal(name):
    if name in TERMINALS:
        return TERMINALS[name]()
    else:
        raise Exception(f"Unknown terminal {name}")
