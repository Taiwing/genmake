# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: yforeau <yforeau@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/12/14 22:53:56 by yforeau           #+#    #+#              #
#    Updated: 2021/09/21 21:01:35 by yforeau          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

############################## COMPILE VAR #####################################

CC			=	gcc
CFLAGS		=	-O -c
NAME		=	Makefile
HDIR		=	includes

############################# GENMAKE INPUT ####################################

PROJDIR		?=	..
HFLAGS		=	-I $(PROJDIR)/$(HDIR)
TYPE		?=	exec
TARG		?=	$(TYPE)
FLAGS		?=	""
DEVFLAGS	?=	""
EXTLIBS		?=	""
SUBCOUNT	?=	0
SUBPATHS	?=	""
SUBTYPES	?=	""
SUBNAMES	?=	""
DEBUG		?=	0

############################### DEBUG VALUES ###################################

debug:
ifeq ($(DEBUG), 1)
	@echo PROJDIR: $(PROJDIR)
	@echo TYPE: $(TYPE)
	@echo NAME: $(NAME)
	@echo FLAGS: $(FLAGS)
	@echo DEVFLAGS: $(DEVFLAGS)
	@echo EXTLIBS: $(EXTLIBS)
	@echo SUBCOUNT: $(SUBCOUNT)
	@echo SUBPATHS: $(SUBPATHS)
	@echo SUBTYPES: $(SUBTYPES)
	@echo SUBNAMES: $(SUBNAMES)
endif

################################# SOURCES ######################################

SRCDIR	=	src
DIRS	=	$(shell find $(PROJDIR)/$(SRCDIR) -type d -name "*")
NBRDIRS	=	$(shell find $(PROJDIR)/$(SRCDIR) -type d -name "*"\
			| wc -l | tr -d '[:blank:]')
CFILES	=	$(shell find $(PROJDIR)/$(SRCDIR) -name "*.c")
NBRCF	=	$(shell find $(PROJDIR)/$(SRCDIR) -name "*.c"\
			| wc -l | tr -d '[:blank:]')

vpath	%.h	$(PROJDIR)/$(HDIR)
vpath	%.c	$(DIRS)

############################## BUILD ###########################################

all: debug $(NAME)

$(NAME): odeps
	./format_odeps.py odeps $(PROJDIR) $(SRCDIR) $(SUBCOUNT) $(SUBPATHS)
	./make_makefile.py odeps $(TYPE) $(TARG) $(PROJDIR) $(HDIR) $(SRCDIR)\
		"$(FLAGS)" "$(DEVFLAGS)" "$(EXTLIBS)" $(NBRDIRS) $(DIRS) $(NBRCF)\
		$(CFILES) $(SUBCOUNT) $(SUBNAMES) $(SUBPATHS) $(SUBTYPES)

odeps: $(CFILES)
	rm -f $@
	$(CC) $(CFLAGS) $(HFLAGS) -MM -MG $^ > $@

############################## CLEANUP #########################################

clean:	
	rm -f odeps

fclean: clean
	rm -f $(PROJDIR)/$(NAME)

re: fclean all

.PHONY: all odeps debug fclean clean re
