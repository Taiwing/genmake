#!/usr/bin/python3

import sys

if len(sys.argv) < 11:
    sys.exit()

odeps = open(sys.argv[1])
targ_type = sys.argv[2]
targ_name = sys.argv[3]
projdir = sys.argv[4]
hdir = sys.argv[5]
srcdir = sys.argv[6].split('/')[-1]
nbr_dirs = int(sys.argv[7])
nbr_files = int(sys.argv[8 + nbr_dirs])
nbr_subs = int(sys.argv[9 + nbr_dirs + nbr_files])

sub_names = []
sub_dirs = []
sub_types = []
for i in range(0, nbr_subs):
    sub_names.append(sys.argv[10 + nbr_dirs + nbr_files + i])
    sub_dirs.append(sys.argv[10 + nbr_dirs + nbr_files + nbr_subs + i])
    sub_types.append(sys.argv[10 + nbr_dirs + nbr_files + (nbr_subs * 2) + i])

dirs = []
pathlen = len(projdir.split('/'))
for i in range(1, nbr_dirs):
    path_dir = sys.argv[8 + i].split('/')
    if len(path_dir) == pathlen + 2:
        dirs.append(path_dir[-1])
    else:
        dirs.append("DO_NOT_APPEND")

makef = open(projdir + "/Makefile", mode="w")

makef.write("############################## COMPILE VAR #####################################\n\n")
makef.write("CC\t\t\t=\tgcc\n")
makef.write("CFLAGS\t\t=\t-Wall -Wextra -Werror\n")
makef.write("#CFLAGS\t\t=\t-g\n")
makef.write("HDIR\t\t=\t" + hdir)
#for i in range(0, nbr_subs):
#    makef.write("HDIR\t\t=\t" + hdir)
makef.write("\nHFLAGS\t\t=\t-I $(HDIR)\n")

makef.write("NAME\t\t=\t")
if targ_type != "lib" or (len(targ_name) > 2 and targ_name[-2:] == ".a"):
    makef.write(targ_name + "\n\n")
elif targ_type == "lib":
    makef.write(targ_name + ".a\n\n")

makef.write("############################## SOURCES #########################################\n\n")
makef.write("SRCDIR\t\t\t=\t" + srcdir + "\n\n")
for direc in dirs:
    if direc != "DO_NOT_APPEND" and direc not in sub_dirs:
        makef.write(direc.upper())
        if len(direc) < 5:
           makef.write("DIR\t\t\t=\t")
        elif len(direc) < 9:
            makef.write("DIR\t\t=\t")
        else:
            makef.write("DIR\t=\t")
        makef.write(direc + "\n")
if len(dirs) > 0:
    makef.write("\n")

files = {}
for i in range(0, nbr_dirs - 1):
    if dirs[i] != "DO_NOT_APPEND":
        files[dirs[i]] = []
files[srcdir] = []

for i in range(0, nbr_files):
    raw = sys.argv[9 + nbr_dirs + i].split('/')
    if raw[-2] == "":
        files[srcdir].append(raw[-1])
    elif raw[-2] in files:
        files[raw[-2]].append(raw[-1])

if len(files[srcdir]) > 0:
    makef.write(srcdir.upper() + "C\t\t\t=\t")
    for cfile in files[srcdir]:
        if cfile == files[srcdir][0]:
            makef.write(cfile + "\\\n")
        else:
            makef.write("\t\t\t\t\t" + cfile + "\\\n")
    makef.write("\n")

for i in range(0, nbr_dirs - 1):
    if dirs[i] != "DO_NOT_APPEND" and dirs[i] not in sub_dirs:
        makef.write(dirs[i].upper() + "C")
        if len(dirs[i]) < 3:
            makef.write("\t\t\t\t=\t")
        elif len(dirs[i]) < 7:
            makef.write("\t\t\t=\t")
        else:
            makef.write("\t\t=\t")
        for cfile in files[dirs[i]]:
            if cfile == files[dirs[i]][0]:
                makef.write(cfile + "\\\n")
            else:
                makef.write("\t\t\t\t\t" + cfile + "\\\n")
        makef.write("\n")

makef.write("ODIR\t\t\t=\tobj\n")
real_nbr_dirs = nbr_dirs
for i in range(0, nbr_dirs - 1):
    if dirs[i] == "DO_NOT_APPEND" or dirs[i] in sub_dirs:
        real_nbr_dirs -= 1
if real_nbr_dirs > 1:
    first_line = 1
    for i in range(0, len(dirs)):
        if dirs[i] != "DO_NOT_APPEND" and dirs[i] not in sub_dirs:
            if first_line:
                makef.write("OBJ\t\t\t\t=\t$(patsubst %.c,%.o,$(" + dirs[i].upper() + "C))\\\n")
                first_line = 0
            else:
                makef.write("\t\t\t\t\t$(patsubst %.c,%.o,$(" + dirs[i].upper() + "C))\\\n")
    if len(files[srcdir]) > 0:
        makef.write("\t\t\t\t\t$(patsubst %.c,%.o,$(" + srcdir.upper() + "C))\\\n")
elif len(files[srcdir]) > 0:
    makef.write("OBJ\t\t\t\t=\t$(patsubst %.c,%.o,$(" + srcdir.upper() + "C))\n")
makef.write("\n")

makef.write("vpath\t\t\t%.o\t$(ODIR)\n")
makef.write("vpath\t\t\t%.h\t$(HDIR)\n")
for direc in dirs:
    if direc != "DO_NOT_APPEND" and direc not in sub_dirs:
        makef.write("vpath\t\t\t%.c\t$(SRCDIR)/$(" + direc.upper() + "DIR)\n")
if len(files[srcdir]) > 0:
    makef.write("vpath\t\t\t%.c\t$(SRCDIR)\n")

makef.write("\n############################## BUILD ###########################################\n\n")
makef.write("all: $(NAME)\n\n")
makef.write("$(NAME): $(ODIR) $(OBJ)\n")
if targ_type == "lib":
    makef.write("\tar rc $@ $(patsubst %.o,$(ODIR)/%.o,$(OBJ))\n")
    makef.write("\tranlib $@\n\n")
else:
    makef.write("\t$(CC) $(CFLAGS) -o $@ $(patsubst %.o,$(ODIR)/%.o,$(OBJ))\n\n")

rules = []
for line in odeps:
    rules.append(line)
for line in odeps:
    if line == rules[-2]:
        break
    sp = line.split()
    size = len(sp)
    if size > 2:
        if len(line) > 80:
            sp = line.split()
            length = 0
            for i in range(0, size):
                if i != 1:
                    length += len(sp[i])
                    if i > 0 and length + i + 1 > 80:
                        makef.write("\\\n\t" + sp[i])
                        length = len(sp[i])
                    elif i > 0 and length > len(sp[i - 1]):
                        makef.write(" " + sp[i])
                    else:
                        makef.write(sp[i])
        else:
            for i in range(0, size):
                if i != 1:
                    if i > 0:
                        makef.write(" " + sp[i])
                    else:
                        makef.write(sp[i])
        makef.write("\n")
makef.write(rules[-2] + rules[-1])
makef.write("\n")

makef.write("$(ODIR):\n")
makef.write("\tmkdir -p $@\n\n")

makef.write("############################## CLEANUP #########################################\n\n")
makef.write("clean:\n")
makef.write("\trm -rf $(ODIR)\n\n")

makef.write("fclean: clean\n")
makef.write("\trm -f $(NAME)\n\n")

makef.write("re: fclean all\n\n")
makef.write(".PHONY: all clean fclean re\n")
