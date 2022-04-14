import collections
import utilities
import structures

def tag(repo, name, ref, message):
    with open(utilities.repo_file(repo, f"refs/tags/{name}"), 'w') as f:
        f.write(create_tag(repo,name,ref,message))

def create_tag(repo, name, ref, message):
    teg = structures.Tag(repo)
    kvlm = collections.OrderedDict()
    kvlm[b'commit']=get_ref(repo, ref).encode()
    kvlm[b'']=message.encode()
    teg.kvlm = kvlm
    return utilities.object_write(teg)

def get_ref(repo, ref):
    if(ref == 'HEAD'):
        return utilities.ref_resolve(repo, ref)
    else:
        return ref