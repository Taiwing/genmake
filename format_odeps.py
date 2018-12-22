#!/usr/bin/python3

import sys

if len(sys.argv) < 2:
    sys.exit()

name = str(sys.argv[1])
file = open(name)

rules = []
for line in file:
    rules.append(line)

res = []
for line in rules:
    skip_nl = 0
#    skip_line = 0
    result = ''
    lst = line.split()
    for word in lst:
        if word[-3:] == ".o:":
            result += word
        elif word[-2:] == ".h" or word[-2:] == ".c":
            result += ' '
            path = word.split('/')
            result += path[-1]
        elif word == "\\":
            skip_nl = 1;
    if skip_nl == 0:
        result += '\n'
    res.append(result)

new = open(name, mode="w")
for line in res:
    new.write(line)
new.write("%.o: %.c\n")
new.write("\t$(CC) -c $(CFLAGS) $< $(HFLAGS) -o $(ODIR)/$@\n")
