ifeq ($(OS),Windows_NT)
    ifdef MSYSTEM
        PLATFORM := unix
    else
        PLATFORM := windows
    endif
else
    PLATFORM := unix
endif

ifeq ($(PLATFORM),windows)
    SHELL_CMD        := pwsh.exe
    SCRIPT_EXTENSION := ps1
    SCRIPT_FLAG		 := -File
    COMMAND_FLAG	 := -Command

    DOCKER_OS := $(shell docker info --format "{{.OSType}}" 2>$$null)
    ifeq ($(DOCKER_OS),windows)
        DOCKER_SOCK := //./pipe/docker_engine
    else
        DOCKER_SOCK := /var/run/docker.sock
    endif
else
    SHELL_CMD        := /bin/bash
    SCRIPT_EXTENSION := sh
    SCRIPT_FLAG  	 :=
    COMMAND_FLAG 	 := -c
    DOCKER_SOCK 	 := /var/run/docker.sock
endif

SCRIPTS := ./tools/scripts

.PHONY: init down up

init:
	@$(SHELL_CMD) $(SCRIPT_FLAG) "$(SCRIPTS)/infrastructure/$(SCRIPT_EXTENSION)/init.$(SCRIPT_EXTENSION)"

down: init
	@$(SHELL_CMD) $(SCRIPT_FLAG) "$(SCRIPTS)/infrastructure/$(SCRIPT_EXTENSION)/down.$(SCRIPT_EXTENSION)" \
		"$(SHELL_CMD)" "$(SCRIPT_EXTENSION)" "$(SCRIPT_FLAG)" "$(COMMAND_FLAG)"

up: init down
	@$(SHELL_CMD) $(SCRIPT_FLAG) "$(SCRIPTS)/infrastructure/$(SCRIPT_EXTENSION)/up.$(SCRIPT_EXTENSION)" \
		"$(SHELL_CMD)" "$(SCRIPT_EXTENSION)" "$(SCRIPT_FLAG)" "$(COMMAND_FLAG)"