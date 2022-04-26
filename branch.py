import collections
import utilities
import structures

def branch(repo, name, ref):
    with open(utilities.repo_file(repo, f"refs/heads/{name}"), 'w') as f:
        f.write(create_branch(repo, ref))

def checkout(repo, type, obj):
    if type == 'commit':
        commit = utilities.object_read(repo, obj)
        utilities.set_work_dir(repo, repo.worktree, commit.kvlm[b'tree'].decode())
    if type == 'tag':
        tag = utilities.object_read(repo, obj)
        commit = utilities.object_read(repo, tag.kvlm[b'commit'].decode())
        utilities.set_work_dir(repo, repo.worktree, commit.kvlm[b'tree'].decode())


def create_branch(repo, ref):
    return utilities.ref_resolve(repo, ref)
