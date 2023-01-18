import os
import subprocess
import tempfile


class GitFile(object):
    def __init__(self, local_repo, location):
        self.__line = location.get("line", None)
        self.__column = location.get("column", None)
        os.chdir(local_repo)
        revision = None
        if "revision" in location:
            current_sha = self.__get_commit_sha()
            if current_sha != location["revision"]:
                revision = location["revision"]

        if revision is not None:
            ext = os.path.splitext(location["path"])[1]
            self.__tempfile = tempfile.NamedTemporaryFile(suffix=ext)
            self.__filename = self.__tempfile.name
            self.__tempfile.write(self.__get_file(revision, location["path"]))
            self.__tempfile.flush()
        else:
            self.__filename = os.path.join(local_repo, location["path"])

    def __query_git(self, args):
        try:
            p = subprocess.Popen(["git"] + args, stdout=subprocess.PIPE)
        except EnvironmentError:
            print("Couldn't run git")
            return ""
        res = p.communicate()[0]
        return res.strip()

    def __get_commit_sha(self):
        return self.__query_git(["rev-parse", "HEAD"]).decode("utf-8")

    def __get_file(self, revision, name):
        return self.__query_git(["show", f"{revision}:{name}"])

    def filename(self):
        return self.__filename

    def line(self):
        return self.__line

    def column(self):
        return self.__column
