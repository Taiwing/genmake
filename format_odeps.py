#!/usr/bin/python3

import sys
import genmake_utils as gmu

if len(sys.argv) < 5:
    sys.exit()

name = sys.argv[1]
projd = sys.argv[2].split('/')
srcdir = sys.argv[3]
nbr_subs = int(sys.argv[4])
dirs = []
for i in range(0, nbr_subs):
    cur = list(projd)
    sub = sys.argv[5 + i].split('/')
    for j in range(0, len(sub)):
        cur.append(sub[j])
#    cur.append(srcdir)
#    cur.append(sys.argv[5 + i])
    dirs.append(cur)

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

print("dirs:") #debug
print(dirs) #debug
res = []
for line in rules:
    skip_nl = 0
    skip_line = 0
    result = ''
    lst = line.split()
    for word in lst:
        print(word) #debug
        if word[-2:] == ".c":
            is_it = gmu.is_file_in_subdir(dirs, word.split("/"))
            print("is c file in subdir: " + str(is_it))
        if word[-3:] == ".o:":
            result += word
        elif word[-2:] == ".c" and nbr_subs > 0 and gmu.is_file_in_subdir(dirs, word.split("/")) != 0:
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

new = open(name, mode="w")
for line in res:
    sys.stdout.write(line) #debug
    new.write(line)
new.write("%.o: %.c\n")
new.write("\t$(CC) -c $(CFLAGS) $< $(HFLAGS) -o $(ODIR)/$@\n")
