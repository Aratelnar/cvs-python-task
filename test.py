import difflib
import filecmp
import os
import zlib

with open("test/.cvs/index", 'rb') as f:
    print(f.read())