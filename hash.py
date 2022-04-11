import utilities
import structures
import sys

def cat_file(repo, obj, fmt=None):
    obj = utilities.object_read(repo, utilities.object_find(repo, obj, fmt=fmt))
    sys.stdout.buffer.write(obj.serialize())

def hash_object(args):
    if args.write:
        repo = structures.Repository(".")
    else:
        repo = None

    with open(args.path, "rb") as fd:
        sha = utilities.object_hash(fd, args.type.encode(), repo)
        print(sha)