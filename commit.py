import collections
import os
import utilities
import structures

def add(repo, path):
    with open(utilities.repo_file(repo, '.lasttree'), 'w') as f:
        f.write(get_tree(repo, path))
    

def get_tree(repo, path):
    tree = structures.Tree(repo)
    path = utilities.work_path(repo, path)
    for (dirpath, dirnames, filenames) in os.walk(path):
        items = []
        for file in filenames:
            p = os.path.join(dirpath, file)
            with open(p, 'rb') as f:
                sha = utilities.object_hash(f, b'blob', repo)
                items.append(structures.TreeRecord(b'000000', p.encode(), sha.encode()))
        for dir in dirnames:
            if dir[0] != '.':
                p = os.path.join(dirpath, dir)
                hash = get_tree(repo, p)
                items.append(structures.TreeRecord(b'000000', p.encode(), hash.encode()))
        break
    tree.items = items
    return utilities.object_write(tree)

def commit(repo, message):
    com = create_commit(repo, message)
    with open(utilities.repo_file(repo, 'HEAD'),'r') as head:
        with open(utilities.repo_file(repo, head.read()[5:-1]), 'w') as f:
            f.write(com)

def create_commit(repo, message):
    commit = structures.Commit(repo)
    kvlm = collections.OrderedDict()
    kvlm[b'parent']=utilities.ref_resolve(repo,'HEAD').encode()
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