import os
import re

from configparser import ConfigParser
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlsplit, urlunsplit


def parse_url(url):
    u = urlparse(url)

    if u.scheme != "ddcode":
        raise Exception(f"Unsupported schema {u.scheme}")
    if u.hostname != "open-in-console":
        raise Exception(f"Unsupported action {u.hostname}")

    q = parse_qs(u.query)

    res = {
        "repo": normalize_url(q["origin"][0]),
        "path": q["path"][0],
    }

    for f in ("column", "line", "revision"):
        if f in q:
            res[f] = q[f][0]
    return res


SCP_REGEXP = re.compile("^[a-z0-9_]+@([a-z0-9._-]+):(.*)$", re.IGNORECASE)


def __remove_suffix(s, suffix):
    if s.endswith(suffix):
        return s[: -len(suffix)]
    else:
        return s


def normalize_url(url):
    scheme = ""
    hostname = ""
    port = None
    path = ""

    match = SCP_REGEXP.match(url)
    if match:
        # Check URLs like "git@github.com:user/project.git",
        scheme = "https"
        hostname = match.group(1)
        path = "/" + match.group(2)
    else:
        u = urlsplit(url)
        if u.scheme == "" and u.hostname is None:
            # Try to add a scheme.
            u = urlsplit("https://" + url)  # Default to HTTPS.
            if u.hostname is None:
                return ""

        scheme = u.scheme
        hostname = u.hostname
        port = u.port
        path = u.path

        if scheme not in ("http", "https", "git", "ssh"):
            return ""

        if not scheme.startswith("http"):
            scheme = "https"  # Default to HTTPS.
            port = None

    path = __remove_suffix(path, ".git/")
    path = __remove_suffix(path, ".git")
    path = __remove_suffix(path, "/")

    netloc = hostname
    if port is not None:
        netloc += ":" + str(port)

    return urlunsplit((scheme, netloc, path, "", ""))


def find_repo_urls(path):
    result = []
    for folder in Path(path).rglob(".git"):
        cfg_file = os.path.join(folder, "config")
        if not os.path.exists(cfg_file):
            continue
        cfg = ConfigParser()
        cfg.read(cfg_file)
        try:
            result.append(
                (normalize_url(cfg['remote "origin"']["url"]), os.path.split(folder)[0])
            )
        except KeyError:
            print(f"Git repository has no remote URL: {folder}")
    return result
