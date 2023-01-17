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
