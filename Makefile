# Main
include tools/makefile/main/variables.mk
include tools/makefile/main/defines.mk
# Infrastructure
include tools/makefile/infrastructure/variables.mk
include tools/makefile/infrastructure/defines.mk
include tools/makefile/infrastructure/targets.mk

up: infrastructure-up

down: infrastructure-down

log:
	@$(info SCRIPT_RUNNER = $(SCRIPT_RUNNER))

.PHONY: up down log