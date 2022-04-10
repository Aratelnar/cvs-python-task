import os
import configparser
import utilities

class CvsObject:
    repo = None

    def __init__(self, repo, data=None):
        self.repo=repo

        if data != None:
            self.deserialize(data)

    def serialize(self):
        raise Exception("Unimplemented!")

    def deserialize(self, data):
        raise Exception("Unimplemented!")


class Tree(CvsObject):
    pass


class Commit(CvsObject):
    pass


class Blob(CvsObject):
    pass


class Repository:
    ''''''

    worktree = None
    cvsdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.cvsdir = os.path.join(path, ".cvs")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository %s" % path)

        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = utilities.repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion %s" % vers)