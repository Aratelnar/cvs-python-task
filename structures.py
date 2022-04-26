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
    fmt=b'tree'

    def deserialize(self, data):
        self.items = utilities.tree_parse(data)

    def serialize(self):
        return utilities.tree_serialize(self)


class TreeRecord:
    def __init__(self, mode, path, sha):
        self.mode = mode
        self.path = path
        self.sha = sha


class Tag(CvsObject):
    fmt=b'tag'

    def deserialize(self, data):
        self.kvlm = utilities.kvlm_parse(data)

    def serialize(self):
        return utilities.kvlm_serialize(self.kvlm)


class Commit(CvsObject):
    fmt=b'commit'

    def deserialize(self, data):
        self.kvlm = utilities.kvlm_parse(data)

    def serialize(self):
        return utilities.kvlm_serialize(self.kvlm)


class Blob(CvsObject):
    fmt=b'blob'

    def serialize(self):
        return self.blobdata

    def deserialize(self, data):
        self.blobdata = data


class Repository:

    worktree = None
    cvsdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.cvsdir = os.path.join(path, ".cvs")

        if not (force or os.path.isdir(self.cvsdir)):
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


