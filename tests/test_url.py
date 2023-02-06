import pytest
import os
import tempfile

from dd_view_code_in_console.url import parse_url, normalize_url, find_repo_urls


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
            "ddcode://open-in-console?origin=https://github.com/user/repo/&path=path/in/repo.py",
            {
                "path": "path/in/repo.py",
                "repo": "https://github.com/user/repo",
            },
            None,
        ),
        (
            "ddcode://open-in-console?origin=https://github.com/user/repo/&path=path/in/repo.py&revision=123456ABC&line=42&column=24",
            {
                "path": "path/in/repo.py",
                "repo": "https://github.com/user/repo",
                "revision": "123456ABC",
                "column": "24",
                "line": "42",
            },
            None,
        ),
        (
            "vscode://datadog.datadog-vscode/open?repo=repo&file=path/in/repo.py&uri=https://github.com/user/repo&ref=123456ABC&range=42:24",
            {
                "path": "path/in/repo.py",
                "repo": "https://github.com/user/repo",
                "revision": "123456ABC",
                "column": "24",
                "line": "42",
            },
            None,
        ),
        (
            "vscode://datadog.datadog-vscode/open?repo=repo&file=path/in/repo.py&uri=https://github.com/user/repo&ref=123456ABC&range=42",
            {
                "path": "path/in/repo.py",
                "repo": "https://github.com/user/repo",
                "revision": "123456ABC",
                "line": "42",
            },
            None,
        ),
        (
            "jetbrains://idea/datadog/open-in-ide?origin=https://github.com/user/repo&path=path/in/repo.py:42&revision=123456ABC",
            {
                "path": "path/in/repo.py",
                "repo": "https://github.com/user/repo",
                "revision": "123456ABC",
                "line": "42",
            },
            None,
        ),
        (
            "jetbrains://idea/datadog/open-in-ide?origin=https://github.com/user/repo&path=path/in/repo.py&revision=123456ABC",
            {
                "path": "path/in/repo.py",
                "repo": "https://github.com/user/repo",
                "revision": "123456ABC",
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


@pytest.mark.parametrize(
    "repository_url,expected",
    [
        # Supported schemes.
        (
            "http://github.com/user/project/",
            "https://github.com/user/project",
        ),
        (
            "http://github.com/user/project.git",
            "https://github.com/user/project",
        ),
        (
            "https://github.com/user/project.git",
            "https://github.com/user/project",
        ),
        (
            "git://github.com/user/project.git",
            "https://github.com/user/project",
        ),
        (
            "git@github.com:user/project.git",
            "https://github.com/user/project",
        ),
        (
            "ssh://git@github.com/user/project.git",
            "https://github.com/user/project",
        ),
        (
            "git://github.com/user/project.git/",
            "https://github.com/user/project",
        ),
        # No scheme but valid TLD.
        (
            "github.com/user/project",
            "https://github.com/user/project",
        ),
        # Subdomain preserved.
        (
            "http://www.github.com/user/project.git",
            "https://www.github.com/user/project",
        ),
        # Preserve port for HTTP/HTTPS schemes.
        (
            "http://github.com:8080/user/project.git",
            "https://github.com:8080/user/project",
        ),
        (
            "https://github.com:8080/user/project.git",
            "https://github.com:8080/user/project",
        ),
        # Do not preserve port otherwise.
        (
            "ssh://git@github.com:22/user/project.git",
            "https://github.com/user/project",
        ),
        # Strip credentials.
        (
            "https://gitlab-ci-token:12345AbcDFoo_qbcdef@gitlab.com/user/project.git",
            "https://gitlab.com/user/project",
        ),
        # Not supported.
        (
            "ftp:///path/to/repo.git/",
            "",
        ),
        (
            "/path/to/repo.git/",
            "",
        ),
        (
            "file:///path/to/repo.git/",
            "",
        ),
    ],
)
def test_normalize_url(repository_url, expected):
    assert normalize_url(repository_url) == expected


def test_find_repo_urls():
    def add_repo(path, url):
        d = os.path.join(tmpdir, path)
        os.system(f"mkdir {d}; cd {d}; git init .; git remote add origin {url}")

    with tempfile.TemporaryDirectory() as tmpdir:
        add_repo("d1", "https://github.com/user/repo1")
        add_repo("d2", "git@github.com:user/repo2.git")
        add_repo("d3", "ssh://git@github.com/user/repo3.git")

        res = find_repo_urls(tmpdir)
        assert sorted(res) == sorted(
            [
                ("https://github.com/user/repo1", os.path.join(tmpdir, "d1")),
                ("https://github.com/user/repo2", os.path.join(tmpdir, "d2")),
                ("https://github.com/user/repo3", os.path.join(tmpdir, "d3")),
            ]
        )
