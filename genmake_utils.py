#!/usr/bin/env python3

def is_quoted(string):
    return (string[0] == "\"" and string[-1] == "\"")

def replace_by(string, old, new = ""):
    o = string.find(old)
    while o > -1:
        if o > 0:
            string = string[:o] + new + string[o + len(old):]
        else:
            string = new + string[len(old):]
        o = string.find(old, o + len(new))
    return string

def is_file_in_subdir(dirs, cfile):
    lenpath = len(dirs[0])
    for subdir in dirs:
        if cfile[:lenpath] == subdir:
            return 1
    return 0

