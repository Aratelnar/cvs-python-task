import collections
import os
import utilities
import structures

def add(repo, path):
    # with open(utilities.repo_file(repo, '.lasttree'), 'w') as f:
    #     f.write(f'{get_tree(repo, path)}\n')
    items = []
    get_items(repo, path, items)
    with open(utilities.repo_file(repo, 'index'), "rb") as f:
        str = f.read().split(b'\n')[:-1]
        if str != [b'']:
            it = [(i.split(b' ')[0],i.split(b' ')[1].split(b'\x00')[0],i.split(b'\x00')[1]) for i in str if str != b'']
            for i in it:
                if path.encode() not in i[1]:
                    items.append(structures.TreeRecord(i[0], i[1], i[2]))
    with open(utilities.repo_file(repo, 'index'), "wb") as f:
        for i in items:
            f.write(f'{i.mode.decode()} {i.path.decode()}\x00{i.sha.decode()}\n'.encode())

    # with open(utilities.repo_file(repo, 'index'), 'w') as index:
    #         d1 = collections.OrderedDict()
    #         for line in index.readlines():
    #             name, sha = line.split()
    #             d1[name] = sha
    #
    #         path = utilities.work_path(repo, path)
    #         for (dirpath, dirnames, filenames) in os.walk(path):
    #             for filename in filenames:
    #                 p = os.path.join(dirpath, filename)
    #                 with open(p, 'rb') as f:
    #                     sha = utilities.object_hash(f, b'blob', repo)
    #                     d[filename] = sha
    #
    #         for name, sha in d.items():
    #             index.write(name + ' ' + sha + '\n')


def get_items(repo, path, items):
    path = utilities.work_path(repo, path)
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            p = os.path.join(dirpath, file)
            with open(p, 'rb') as f:
                sha = utilities.object_hash(f, b'blob', repo)
                items.append(structures.TreeRecord(b'000000', p.replace(f'{repo.worktree}\\', '').encode(), sha.encode()))

        for dir in dirnames:
            if dir[0] != '.':
                p = os.path.join(dirpath, dir)
                get_items(repo, p, items)
        break

def commit(repo, message):
    com = create_commit(repo, message)
    with open(utilities.repo_file(repo, 'HEAD'), 'r') as head:
        with open(utilities.repo_file(repo, head.read()[5:-1]), 'w') as f:
            f.write(f'{com}\n')

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []
        self.sha = b''
        self.mode = b'000000'

    def get_sha(self,repo):
        if self.sha != b'':
            return self.sha
        tree = structures.Tree(repo)
        list = []
        for i in self.children:
            list.append(structures.TreeRecord(i.mode, i.name, i.get_sha(repo)))
        tree.items = list
        return utilities.object_write(tree).encode()

    def children_names(self):
        return [i.name for i in self.children]

    def get_child(self, name):
        list = [(i, i.name) for i in self.children]
        for j in list:
            if j[1] == name:
                return j[0]
        return None
    pass

def create_tree(repo):
    root = TreeNode(".")
    with open(utilities.repo_file(repo, 'index'), 'rb') as f:
        str = f.read().split(b'\n')
        str = str[:-1]
        for line in str:
            mode, path, sha = line.split(b' ')[0], line.split(b' ')[1].split(b'\x00')[0], line.split(b'\x00')[1]
            tokens = path.split(b'\\')
            place = root
            for token in tokens:
                if token == '.':
                    continue
                if token not in place.children_names():
                    place.children.append(TreeNode(token))
                place = place.get_child(token)
            place.sha = sha
    with open(utilities.repo_file(repo, '.lasttree'), 'w') as f:
        f.write(f'{root.get_sha(repo).decode()}\n')
                
    pass

def create_commit(repo, message):
    create_tree(repo)
    commit = structures.Commit(repo)
    kvlm = collections.OrderedDict()
    kvlm[b'parent']=utilities.ref_resolve(repo, 'HEAD').encode()
    kvlm[b'tree']=utilities.ref_resolve(repo, '.lasttree').encode()
    kvlm[b'']=message.encode()
    commit.kvlm = kvlm
    return utilities.object_write(commit)

def initial_commit(repo):
    commit = structures.Commit(repo)
    kvlm = collections.OrderedDict()
    kvlm[b'']=b"Initial Commit"
    commit.kvlm = kvlm
    return utilities.object_write(commit)