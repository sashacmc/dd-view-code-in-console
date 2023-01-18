import argparse
import os

from .config import Config
from .editor import get_editor
from .gitfile import GitFile
from .terminal import get_terminal
from .url import parse_url, find_repo_urls


def scan_repositories(cfg, path):
    repos = find_repo_urls(path)
    cfg.add_repositories(repos)
    print(f"Found {len(repos)} repositories")


def open_url(cfg, url):
    terminal = get_terminal(cfg.get_terminal())
    editor = get_editor(cfg.get_editor())
    location = parse_url(url)
    local_repo = cfg.get_local_path(location["repo"])
    f = GitFile(local_repo, location)
    terminal.open(editor, f)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="python3 -m dd_view_code_in_console",
        description="Open source code from Datadog in the console",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-o", "--open", help="Open URL", type=str)
    group.add_argument("-s", "--scan", help="Scan for local git reposotories", type=str)
    parser.add_argument(
        "-c",
        "--config",
        help="Config file",
        default="~/.dd_view_code_in_terminal.cfg",
        type=str,
    )
    return parser, parser.parse_args()


def main():
    parser, args = parse_args()
    cfg = Config(os.path.expanduser(args.config))
    if args.open:
        open_url(cfg, args.open)
    elif args.scan:
        scan_repositories(cfg, args.scan)
    else:
        parser.print_help()


main()
