import os

from configparser import ConfigParser
from glob import glob
from urllib.parse import urlparse, parse_qs


def parse_url(url):
    u = urlparse(url)

    if u.scheme != "ddcode":
        raise Exception(f"Unsupported schema {u.scheme}")
    if u.hostname != "open-in-console":
        raise Exception(f"Unsupported action {u.hostname}")

    q = parse_qs(u.query)

    res = {
        "repo": q["origin"][0],
        "path": q["path"][0],
    }

    for f in ("column", "line", "revision"):
        if f in q:
            res[f] = q[f][0]
    return res


def normalize_url(url):
    return url


def find_repo_urls(path):
    result = []
    for folder in glob(os.path.join(os.path.abspath(path), "**/.git")):
        cfg = ConfigParser()
        cfg.read(os.path.join(folder, "config"))
        result.append((normalize_url(cfg['remote "origin"']["url"]), os.path.split(folder)[0]))
    return result
