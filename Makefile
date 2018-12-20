# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: yforeau <yforeau@student.42.fr>            +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2018/12/14 22:53:56 by yforeau           #+#    #+#              #
#    Updated: 2018/12/20 22:53:24 by yforeau          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

############################## COMPILE VAR #####################################

CC			=	gcc
CFLAGS		=	-O -c -Wall -Wextra -Werror
PROJDIR		?=	..
HDIR		=	includes
HFLAGS		=	-I $(PROJDIR)/$(HDIR)
# can be exec or lib:
TYPE		?=	exec
# can be whatevs:
TARG		?=	$(TYPE)
NAME		=	Makefile

############################## SOURCES #########################################

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

all: $(NAME)

$(NAME): odeps
	./format_odeps.py odeps
	./make_makefile.py odeps $(TYPE) $(TARG) $(PROJDIR) $(HDIR) $(SRCDIR)\
		$(NBRDIRS) $(DIRS) $(NBRCF) $(CFILES)

odeps: $(CFILES)
	rm -f $@
	$(CC) $(CFLAGS) $(HFLAGS) -MM -MG $^ > $@

############################## CLEANUP #########################################

clean:	
	rm -f odeps

fclean: clean
	rm -f $(PROJDIR)/$(NAME)

re: fclean all

.PHONY: all odeps fclean clean re
