import os
import re

from configparser import ConfigParser
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlsplit, urlunsplit


def __parse_ddcode_url(u, q):
    if u.hostname != "open-in-console":
        raise Exception(f"Unsupported action {u.hostname}")

    res = {
        "repo": normalize_url(q["origin"][0]),
        "path": q["path"][0],
    }

    for f in ("column", "line", "revision"):
        if f in q:
            res[f] = q[f][0]
    return res


def __parse_vscode_url(u, q):
    if u.hostname != "datadog.datadog-vscode":
        raise Exception(f"Unsupported url {u.hostname}")
    if u.path != "/open":
        raise Exception(f"Unsupported action {u.path}")

    res = {
        "repo": normalize_url(q["uri"][0]),
        "path": q["file"][0],
    }

    if "ref" in q:
        res["revision"] = q["ref"][0]
    if "range" in q:
        r = q["range"][0]
        p = r.find(":")
        if p > 0:
            res["line"] = r[:p]
            res["column"] = r[p + 1 :]
        else:
            res["line"] = r

    return res


def __parse_jetbrains_url(u, q):
    if u.hostname != "idea":
        raise Exception(f"Unsupported action {u.hostname}")
    if u.path != "/datadog/open-in-ide":
        raise Exception(f"Unsupported action {u.path}")

    res = {
        "repo": normalize_url(q["origin"][0]),
    }

    path = q["path"][0]
    p = path.find(":")
    if p > 0:
        res["path"] = path[:p]
        res["line"] = path[p + 1 :]
    else:
        res["path"] = path

    if "revision" in q:
        res["revision"] = q["revision"][0]

    return res


SCHEMAS = {
    "ddcode": __parse_ddcode_url,
    "vscode": __parse_vscode_url,
    "jetbrains": __parse_jetbrains_url,
}


def parse_url(url):
    u = urlparse(url)
    q = parse_qs(u.query)

    if u.scheme in SCHEMAS:
        return SCHEMAS[u.scheme](u, q)
    else:
        raise Exception(f"Unsupported schema {u.scheme}")


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
            port = None
        scheme = "https"  # Default to HTTPS.

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
