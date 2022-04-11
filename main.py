import argparse
import os
import re
import sys
import difflib
import utilities
import init
import hash

def add_init():
    argsp = argsubparsers.add_parser("init")
    argsp.add_argument("path",
                       metavar="directory",
                       nargs='?',
                       default='.')

def add_hash_cat():
    argsp = argsubparsers.add_parser("cat-file")
    argsp.add_argument("type",
                   metavar="type",
                   choices=["blob", "commit", "tag", "tree"],
                   help="Specify the type")
    argsp.add_argument("object",
                   metavar="object",
                   help="The object to display") 

def add_hash_hash():
    argsp = argsubparsers.add_parser("hash-object")

    argsp.add_argument("-t",
                   metavar="type",
                   dest="type",
                   choices=["blob", "commit", "tag", "tree"],
                   default="blob",
                   help="Specify the type")

    argsp.add_argument("-w",
                   dest="write",
                   action="store_true",
                   help="Actually write the object into the database")

    argsp.add_argument("path",
                   help="Read object from <file>")

argparser = argparse.ArgumentParser(description="")
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True
add_init()
add_hash_cat()
add_hash_hash()


def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if   args.command == "init"         : init.repo_create(args.path)
    elif args.command == "cat-file"     : hash.cat_file(utilities.repo_find(), args.object, fmt=args.type.encode())
    #elif args.command == "checkout"    : cmd_checkout(args)
    #elif args.command == "commit"      : cmd_commit(args)
    elif args.command == "hash-object"  : hash.hash_object(args)
    #elif args.command == "add "        : cmd_add(args)
    #elif args.command == "log"         : cmd_log(args)
    #elif args.command == "ls-tree"     : cmd_ls_tree(args)
    #elif args.command == "merge"       : cmd_merge(args)
    #elif args.command == "rebase"      : cmd_rebase(args)
    #elif args.command == "rev-parse"   : cmd_rev_parse(args)
    #elif args.command == "rm"          : cmd_rm(args)
    #elif args.command == "show-ref"    : cmd_show_ref(args)
    #elif args.command == "tag"         : cmd_tag(args)

if __name__ == '__main__':
    main()