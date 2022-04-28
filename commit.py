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
                if i[1] not in (j.path for j in items):
                    items.append(structures.TreeRecord(i[0], i[1], i[2]))
    with open(utilities.repo_file(repo, 'index'), "wb") as f:
        for i in items:
            f.write(f'{i.mode.decode()} {i.path.decode()}\x00{i.sha.decode()}\n'.encode())
    pass

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
                get_tree(repo, p, items)
        break

def commit(repo, message):
    com = create_commit(repo, message)
    with open(utilities.repo_file(repo, 'HEAD'), 'r') as head:
        with open(utilities.repo_file(repo, head.read()[5:-1]), 'w') as f:
            f.write(f'{com}\n')

def create_commit(repo, message):
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