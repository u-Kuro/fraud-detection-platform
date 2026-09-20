# Prevent MSYS/MinGW conversion of Unix paths to Windows paths
export MSYS_NO_PATHCONV 		 		:= 1
# Project
export ROOT_DIRECTORY			 		:= $(CURDIR)
# Scripts
SCRIPT_DIRECTORY     	   		 		:= tools/scripts
MAKEFILE_SCRIPT_DIRECTORY  	 	 		:= $(SCRIPT_DIRECTORY)/makefile
INFRASTRUCTURE_SCRIPT_DIRECTORY  		:= $(SCRIPT_DIRECTORY)/infrastructure
# Infrastructure
export INFRASTRUCTURE_DOCKERFILE 		:= infrastructure/Dockerfile
export INFRASTRUCTURE_IMAGE 	 		:= fraud-detection-platform-infrastructure

ifeq ($(OS), Windows_NT)
    ifdef MSYSTEM
        PLATFORM  := unix
    else
        PLATFORM  := windows
    endif
else
    PLATFORM  := unix
endif

ifeq ($(PLATFORM), windows)
    SCRIPT_RUNNER    := pwsh -NoProfile -ExecutionPolicy Bypass -File
	SCRIPT_FOLDER	 := pwsh
    SCRIPT_EXTENSION := ps1
    COMMAND_RUNNER	 := pwsh -NoProfile -ExecutionPolicy Bypass -Command
	DOCKER_OS 		 := $(shell docker info --format "{{.OSType}}")
	ifeq ($(DOCKER_OS), windows)
		export DOCKER_SOCK := //./pipe/docker_engine
	else
		export DOCKER_SOCK := /var/run/docker.sock
	endif
else
    SCRIPT_RUNNER      := /bin/bash
	SCRIPT_FOLDER	   := bash
    SCRIPT_EXTENSION   := sh
	export DOCKER_SOCK := /var/run/docker.sock
endif

# Script Runner
define RUN_BASH_SCRIPT
$(SCRIPT_RUNNER) "$(1)/$(2).sh"
endef
define RUN_SCRIPT
$(SCRIPT_RUNNER) "$(1)/$(SCRIPT_FOLDER)/$(2).$(SCRIPT_EXTENSION)"
endef

define FORMAT_SCRIPT_ARGUMENTS
$(if $(filter $(PLATFORM),windows),"-$(1):$(2)","$(2)")
endef

# > Makefile
define RUN_MAKEFILE_SCRIPT
$(call RUN_SCRIPT,$(MAKEFILE_SCRIPT_DIRECTORY),$(1))
endef

define BUILD_IMAGE
$(if $(filter $(IS_INSIDE_FRAUD_DETECTION_PLATFORM_DOCKER),true),,$(call RUN_MAKEFILE_SCRIPT,build-image) $(call FORMAT_SCRIPT_ARGUMENTS,DOCKERFILE,$(1)) $(call FORMAT_SCRIPT_ARGUMENTS,IMAGE,$(2)))
endef

# > Makefile
define RUN_INFRASTRUCTURE_SCRIPT
$(call RUN_BASH_SCRIPT,$(INFRASTRUCTURE_SCRIPT_DIRECTORY),$(1))
endef

.PHONY: init down up \
	build-infrastructure-image \
	init-infrastructure down-infrastructure up-infrastructure \
	terraform-init terraform-destroy terraform-apply

init: init-infrastructure

down: down-infrastructure

up: up-infrastructure

build-infrastructure-image:
	@$(call BUILD_IMAGE,infrastructure/Dockerfile,fraud-detection-platform-infrastructure)

init-infrastructure: build-infrastructure-image
	@$(call RUN_MAKEFILE_SCRIPT,run-infrastructure-phony) terraform-init

down-infrastructure: build-infrastructure-image
	@$(call RUN_MAKEFILE_SCRIPT,run-infrastructure-phony) terraform-destroy

up-infrastructure: build-infrastructure-image
	@$(call RUN_MAKEFILE_SCRIPT,run-infrastructure-phony) terraform-apply

terraform-init:
	@$(call RUN_INFRASTRUCTURE_SCRIPT,init)

terraform-destroy: terraform-init
	@$(call RUN_INFRASTRUCTURE_SCRIPT,down)

terraform-apply: terraform-init terraform-destroy
	@$(call RUN_INFRASTRUCTURE_SCRIPT,up)

log:
	@$(info SCRIPT_RUNNER	 = $(SCRIPT_RUNNER))
#	@$(info SCRIPT_FOLDER 	 = $(SCRIPT_FOLDER))
#	@$(info SCRIPT_EXTENSION = $(SCRIPT_EXTENSION))
#	@$(info DOCKER_OS        = $(DOCKER_OS))
#	@$(info DOCKER_SOCK      = $(DOCKER_SOCK))
