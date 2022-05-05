import collections
import os
import utilities
import structures
import shutil

def branch(repo, name, ref):
    with open(utilities.repo_file(repo, f"refs/heads/{name}"), 'w') as f:
        f.write(create_branch(repo, ref))

def checkout(repo, type, obj):
    remove_work_dir(repo)
    if type == 'commit':
        commit = utilities.object_read(repo, obj)
        utilities.set_work_dir(repo, repo.worktree, commit.kvlm[b'tree'].decode())
        write_head(repo, obj)
    if type == 'tag':
        tag = utilities.object_read(repo, obj)
        commit = utilities.object_read(repo, tag.kvlm[b'commit'].decode())
        utilities.set_work_dir(repo, repo.worktree, commit.kvlm[b'tree'].decode())
        write_head(repo, tag.kvlm[b'commit'].decode())

def write_head(repo, data):
    with open(utilities.repo_file(repo, 'HEAD'), 'w') as f:
        f.write(data)    

def remove_work_dir(repo):
    address, dirs, files = next(os.walk(repo.worktree))
    for dir in dirs:
        if dir != '.cvs':
            shutil.rmtree(utilities.repo_dir(repo, dir))
    for file in files:
        os.remove(utilities.work_path(repo, file))

def create_branch(repo, ref):
    return utilities.ref_resolve(repo, ref)
