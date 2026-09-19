ifeq ($(OS), Windows_NT)
    ifdef MSYSTEM
        PLATFORM := "unix"
    else
        PLATFORM := "windows"
    endif
else
    PLATFORM := "unix"
endif

ifeq ($(PLATFORM), "windows")
    SHELL_CMD          := "pwsh"
    SCRIPT_EXTENSION   := "ps1"
    SCRIPT_FLAG		   := "-File"
    COMMAND_FLAG	   := "-Command"

    DOCKER_OS := $(shell docker info --format "{{.OSType}}")
    ifeq ($(DOCKER_OS), "windows")
        DOCKER_SOCK := "//./pipe/docker_engine"
    else
        DOCKER_SOCK := "/var/run/docker.sock"
    endif
else
    SHELL_CMD          := "/bin/bash"
    SCRIPT_EXTENSION   := "sh"
    SCRIPT_FLAG  	   := ""
    COMMAND_FLAG 	   := "-c"
    DOCKER_SOCK 	   := "/var/run/docker.sock"
endif

SCRIPTS := "./tools/scripts"
define FORMAT_SCRIPT_ARGUMENTS
$(if $(filter "windows", $(PLATFORM)),"-$(1):$(2)","$(2)")
endef

.PHONY: init down up

init:
	@$(SHELL_CMD) $(SCRIPT_FLAG) "$(SCRIPTS)/infrastructure/$(SCRIPT_EXTENSION)/init.$(SCRIPT_EXTENSION)"

down: init
	@$(SHELL_CMD) $(SCRIPT_FLAG) "$(SCRIPTS)/infrastructure/$(SCRIPT_EXTENSION)/down.$(SCRIPT_EXTENSION)" \
		$(call FORMAT_SCRIPT_ARGUMENTS,SHELL_CMD,$(SHELL_CMD)) \
		$(call FORMAT_SCRIPT_ARGUMENTS,SCRIPT_EXTENSION,$(SCRIPT_EXTENSION)) \
		$(call FORMAT_SCRIPT_ARGUMENTS,SCRIPT_FLAG,$(SCRIPT_FLAG)) \
		$(call FORMAT_SCRIPT_ARGUMENTS,COMMAND_FLAG,$(COMMAND_FLAG))

up: init down
	@$(SHELL_CMD) $(SCRIPT_FLAG) "$(SCRIPTS)/infrastructure/$(SCRIPT_EXTENSION)/up.$(SCRIPT_EXTENSION)" \
		$(call FORMAT_SCRIPT_ARGUMENTS,SHELL_CMD,$(SHELL_CMD)) \
		$(call FORMAT_SCRIPT_ARGUMENTS,SCRIPT_EXTENSION,$(SCRIPT_EXTENSION)) \
		$(call FORMAT_SCRIPT_ARGUMENTS,SCRIPT_FLAG,$(SCRIPT_FLAG)) \
		$(call FORMAT_SCRIPT_ARGUMENTS,COMMAND_FLAG,$(COMMAND_FLAG))