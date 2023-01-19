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
        from threading import Thread

        cmd = self._get_command(editor, gitfile)

        def run_term():
            subprocess.run(
                ("/usr/bin/open", "-W", "-n", "-a", "/Applications/iTerm.app")
            )

        th_run = Thread(target=run_term)
        th_run.start()

        async def main(connection):
            app = await iterm2.async_get_app(connection)
            await app.async_activate()

            window = app.current_terminal_window
            session = app.current_terminal_window.current_tab.current_session
            await session.async_send_text(f"{cmd}; exit;\n")

        iterm2.run_until_complete(main, True)
        th_run.join()


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
