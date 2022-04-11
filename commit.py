import os
import utilities
import structures

def add(repo, path):
    print(get_tree(repo, path))
    

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