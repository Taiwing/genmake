# genmake

This tool is a Makefile generator for C projects. It builds a fully working
Makefile, in compliance with 42's standard, with a simple one word command. This
makes develoment easier and faster.

## Setup

```shell
# clone it
git clone https://github.com/Taiwing/genmake
cd genmake/
# create an alias in your shell
alias genmake="$(pwd)/genmake"
# run it in your project directory
cd ~/my_c_project && genmake
```

## Pre-requisites

- The project must be developped in C
- There must be a src/ directory where every C file will be located (either
  directly at the root of the directory or in subdirectories).
- 1 is the level max of subdirectories permitted in src/ except if a
  subdirectory is specified as a subproject.
- If there are subprojects they are supposed to have Makefiles with
  the rules required by 42's norme (except if --recursive is set).
- The headers will be in a directory named includes/ located
  at the root of the project.
- Every include directive of a source header must not include the path,
  only the file name.

> If any of these requirements is not met genmake will not be able to produce a
> working makefile for the project.

## Usage

```
Usage:
	genmake [-t type] [-n name] [-f flags] [-D devflags] [-s[t | n | tn] path]
	genmake [-vdh] [path]

Options:
    -h, --help
        Print this.

    -t, --type
        The next argument is the type of the target that the generated makefile
        will create. That value can be 'exec 'or 'lib', where the first one
        refers to a program, and the second to a library (compiles a program by
        default). The type will be set to library if a name is provided and it
        ends with '.a' suffix.

    -n, --name
        Name of the target ('exec' by default or 'lib.a' if type is 'lib'). A
        suffix '.a' will be added to the name if the type of the target is 'lib'
        and the extension is not present.

    -v, --verbose
        Print additional informations.

    -d, --debug
        Print even more additional informations.

    -s, --subproject
        Declare a directory as a subproject with its own Makefile. A rule to
        make it will be added to the final Makefile. --type and --name can be
        used with --subproject. If no type is provided it will default to lib.

    -f, --flags
        Set Makefile's CFLAGS to a custom value.

    -D, --devflags
        Set flags to add to Makefile's CFLAGS for uncommented version (dev).

    -l, --libs
        Add external libraries (eg: '-ltermcap -lpthread -lpcap').

Advanced:
    If genmake is not provided any options and arguments it will check if a
    '.genmake' file exists at the root of the current directory. If it there is
    such a file genmake will use its content as options and arguments. Otherwise
    the defaults will be used to generate the Makefile. This is useful to avoid
    retyping the same command over and over especially in cases where specific
    compilation flags must be set and/or the project has a lot dependencies.
```
