#####################################################################
###################Shrijan's Own version of Git######################
#####################################################################
import argparse                 #to parse command line arguments
import collections              #for an OrderedDict
import configparser             #Git uses a configuration file format that is basically Microsoft’s INI format. The configparser module can read and write these files.
import  grp, pwd                #to read users/group databaseon Unix. Git saves numerical owner/grup ID of files. We'll display that as text.
from fnmatch import fnmatch     #for .gitignore filename matching patterns
from datetime import datetime   #date and time manipulation
import hashlib                  #for SHA-1 hash function
import math                     #for math
import os                       #for filesystem abstraction routines
import re                       #for regular expressions :/
import sys                      #to access command line arguments
import zlib                     #to compress

#################################################################

#To parse and handle commands and subcommands like commit, init because you do git "COMMAND" not just git
argparser = argparse.ArgumentParser(description= "THE content tracker")
argsybparsers = argparser.add_subparsers(title="Commands", dest="command")       
argsybparsers.required= True #a subcomand is required


def main(argv=sys.argv[1:]):
    args =argparser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")



 #Git Repo#
class gitRepository (object):
   
   worktree = None
   gitdir = None
   conf = None


   def __init__(self,path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path,".git")

        #checks if the .git directory exists unless you specifically tell it not to (by setting force to True)
        #if its not a repository or force is false (not(false or false) = true) it raises an exception
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository %s" % path)
        
        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion %s" % vers)



        
