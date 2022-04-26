import difflib
import filecmp
import zlib


with open('test/.cvs/objects/63/c1d396edd3726bbcfbf38fdfc90e17612a7b32', 'wb') as f:
    # print(zlib.decompress(f.read()))
    f.write(zlib.compress(b'commit 95\x00parent b1461154bf3722923f7a92af83e8adcbb926279b\ntree 90a2b20f8ac2ad289e7f9a8a4ceba2399d68f6bb\n\n'))