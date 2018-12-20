#!/usr/bin/python3

import sys

if len(sys.argv) < 2:
    sys.exit()

name = str(sys.argv[1])
file = open(name)

rules = []
for line in file:
    rules.append(line)

new = open(name, mode="w")
for line in rules:
    skip = 0
    lst = line.split()
    for word in lst:
        if word[-3:] == ".o:":
            new.write(word)
        elif word[-2:] == ".h" or word[-2:] == ".c":
            new.write(' ')
            path = word.split('/')
            new.write(path[-1])
        elif word == "\\":
            skip = 1;
    if skip == 0:
        new.write('\n')
new.write("%.o: %.c\n")
new.write("\t$(CC) -c $(CFLAGS) $< $(HFLAGS) -o $(ODIR)/$@\n")
