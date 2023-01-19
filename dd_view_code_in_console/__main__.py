import argparse
import os

# for support py2app and normal packaging
try:
    from .config import Config
    from .editor import get_editor
    from .gitfile import GitFile
    from .terminal import get_terminal
    from .url import parse_url, find_repo_urls
except (ImportError, ModuleNotFoundError):
    from config import Config
    from editor import get_editor
    from gitfile import GitFile
    from terminal import get_terminal
    from url import parse_url, find_repo_urls


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
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("url", nargs='?', help="URL to open in console editor")
    parser.add_argument(
        "-s",
        "--scan",
        help="Path to scan for local git reposotories",
        type=str,
    )
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
    if args.scan:
        scan_repositories(cfg, args.scan)
    elif args.url:
        open_url(cfg, args.url)
    else:
        parser.print_help()


try:
    main()
except Exception as ex:
    import traceback

    with open("/tmp/dd-view-code-in-console-crash-log.txt", "w") as f:
        traceback.print_exception(ex, file=f)
