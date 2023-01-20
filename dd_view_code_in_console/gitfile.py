import os
import subprocess
import tempfile


class GitFile(object):
    def __init__(self, local_repo, location):
        self.__line = location.get("line", None)
        self.__column = location.get("column", None)
        repo = location["repo"]
        if not os.path.exists(local_repo):
            self.__report_error(f"Repository not found: {repo}")
            return

        os.chdir(local_repo)
        revision = None
        if "revision" in location:
            try:
                current_sha = self.__get_commit_sha()
            except Exception as ex:
                self.__report_error(
                    f"Can't get commit hash for repo {repo}:{local_repo}: {str(ex)}"
                )
            if current_sha != location["revision"]:
                revision = location["revision"]

        path = location["path"]
        if revision is not None:
            ext = os.path.splitext(path)[1]
            try:
                data = self.__get_file(revision, path)
                self.__write_tempfile(ext, data)
            except Exception as ex:
                self.__report_error(
                    f"Can't get file {path} from git repo {repo}:{local_repo}: {str(ex)}"
                )
        else:
            self.__filename = os.path.join(local_repo, path)

    def __write_tempfile(self, ext, data):
        self.__tempfile = tempfile.NamedTemporaryFile(suffix=ext)
        self.__tempfile.write(data)
        self.__tempfile.flush()
        self.__filename = self.__tempfile.name

    def __report_error(self, message):
        self.__write_tempfile(".txt", message.encode("UTF-8"))

    def __query_git(self, args):
        try:
            p = subprocess.Popen(["git"] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except EnvironmentError:
            Exception("Couldn't run git")
        res, err = p.communicate()
        if p.returncode != 0:
            raise Exception(err.decode("UTF-8"))
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
