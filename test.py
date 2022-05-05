import difflib
import filecmp
import os
import zlib

with open("test/.cvs/abc", 'w') as f:
    f.write('test abc')