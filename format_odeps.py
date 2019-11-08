#!/usr/bin/env python3

import sys
import genmake_utils as gmu

################################ get arguments #################################

if len(sys.argv) < 5:
    sys.exit()

name = sys.argv[1]
projdir = sys.argv[2].split('/')
srcdir = sys.argv[3]
subcount = int(sys.argv[4])
subpaths = []
for i in range(0, subcount):
    cur = list(projdir)
    sub = sys.argv[5 + i].split('/')
    for j in range(0, len(sub)):
        cur.append(sub[j])
    subpaths.append(cur)

############################### load odeps file ################################

file = open(name)
temp = ""
rules = []
for line in file:
    if "\\\n" in line:
        temp += gmu.replace_by(line, "\\\n")
    elif temp == "":
        rules.append(line)
    else:
        rules.append(temp + line)
        temp = ""

################################# format odeps #################################

res = []
for line in rules:
    skip_nl = 0
    skip_line = 0
    result = ''
    lst = line.split()
    for word in lst:
        if word[-3:] == ".o:":
            result += word
        elif word[-2:] == ".c" and subcount > 0 and gmu.is_file_in_subdir(subpaths, word.split("/")) != 0:
            skip_line = 1
        elif word[-2:] == ".h" or word[-2:] == ".c":
            result += ' '
            path = word.split('/')
            result += path[-1]
        elif word == "\\":
            skip_nl = 1
    if skip_nl == 0:
        result += '\n'
    if skip_line == 0:
        res.append(result)

################################# write odeps ##################################

new = open(name, mode="w")
for line in res:
    new.write(line)
new.write("%.o: %.c\n")
new.write("\t$(CC) -c $(CFLAGS) $< $(HFLAGS) -o $(ODIR)/$@\n")
