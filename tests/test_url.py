import pytest
import os
import tempfile

from dd_view_code_in_console.url import parse_url, find_repo_urls


@pytest.mark.parametrize(
    "repository_url,expected,error",
    [
        ("none", {}, "Unsupported schema "),
        ("http://github.com/user/project", {}, "Unsupported schema http"),
        ("ddcode://some.name?arg=test", {}, "Unsupported action some.name"),
        (
            "ddcode://open-in-console?revision=123456ABC&line=42&column=24",
            {},
            "'origin'",
        ),
        (
            "ddcode://open-in-console?origin=https://github.com:user/repo/&path=path/in/repo.py",
            {
                "path": "path/in/repo.py",
                "repo": "https://github.com:user/repo/",
            },
            None,
        ),
        (
            "ddcode://open-in-console?origin=https://github.com:user/repo/&path=path/in/repo.py&revision=123456ABC&line=42&column=24",
            {
                "path": "path/in/repo.py",
                "repo": "https://github.com:user/repo/",
                "revision": "123456ABC",
                "column": "24",
                "line": "42",
            },
            None,
        ),
    ],
)
def test_parse_url(repository_url, expected, error):
    if error is None:
        assert parse_url(repository_url) == expected
    else:
        with pytest.raises(Exception) as excinfo:
            parse_url(repository_url)
        assert str(excinfo.value) == error


def test_find_repo_urls():
    def add_repo(path, url):
        d = os.path.join(tmpdir, path)
        os.system(f"mkdir {d}; cd {d}; git init .; git remote add origin {url}")

    with tempfile.TemporaryDirectory() as tmpdir:
        add_repo("d1", "https://github.com/user/repo")
        add_repo("d2", "git@github.com:user/project.git")
        add_repo("d3", "ssh://git@github.com/user/project.git")

        res = find_repo_urls(tmpdir)
        assert sorted(res) == sorted(
            [
                ("https://github.com/user/repo", os.path.join(tmpdir, "d1")),
                ("git@github.com:user/project.git", os.path.join(tmpdir, "d2")),
                ("ssh://git@github.com/user/project.git", os.path.join(tmpdir, "d3")),
            ]
        )
