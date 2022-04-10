import os
import structures
import utilities

def repo_create(path):
    """Create a new repository at path."""

    repo = structures.Repository(path, True)

    # First, we make sure the path either doesn't exist or is an
    # empty dir.

    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception ("%s is not a directory!" % path)
        if os.listdir(repo.worktree):
            raise Exception("%s is not empty!" % path)
    else:
        os.makedirs(repo.worktree)

    assert(utilities.repo_dir(repo, "branches", mkdir=True))
    assert(utilities.repo_dir(repo, "objects", mkdir=True))
    assert(utilities.repo_dir(repo, "refs", "tags", mkdir=True))
    assert(utilities.repo_dir(repo, "refs", "heads", mkdir=True))

    # .git/description
    with open(utilities.repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # .git/HEAD
    with open(utilities.repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    with open(utilities.repo_file(repo, "config"), "w") as f:
        config = utilities.repo_default_config()
        config.write(f)

    return repo