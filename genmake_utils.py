#!/usr/bin/python3

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
