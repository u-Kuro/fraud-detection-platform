# Prevent MSYS/MinGW conversion of Unix paths to Windows paths
export MSYS_NO_PATHCONV := 1

# Shell
ifeq ($(OS), Windows_NT)
    SHELL_COMMAND := powershell.exe
else
    SHELL_COMMAND := /bin/bash
endif
ifeq ($(SHELL_COMMAND), powershell.exe)
    SCRIPT_RUNNER    := $(SHELL_COMMAND) -NoProfile -ExecutionPolicy Bypass -File
	SCRIPT_FOLDER	 := powershell
    SCRIPT_EXTENSION := ps1
else
    SCRIPT_RUNNER    := $(SHELL_COMMAND)
	SCRIPT_FOLDER	 := bash
    SCRIPT_EXTENSION := sh
endif

# Directories
export ABSOLUTE_ROOT_DIRECTORY := $(CURDIR)
MAKEFILE_DIRECTORY 	  		   := tools/makefile
MAIN_DIRECTORY 		  		   := $(MAKEFILE_DIRECTORY)/main
MAIN_SCRIPT_DIRECTORY 		   := $(MAIN_DIRECTORY)/scripts