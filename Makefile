ifeq ($(OS),Windows_NT)
    SHELL := pwsh.exe
else
    SHELL := pwsh
endif
.SHELLFLAGS := -NoProfile -NonInteractive -Command

SCRIPTS := ./tools/scripts

.PHONY: init down up

init:
	@& '$(SCRIPTS)/infrastructure/init.ps1'

down: init
	@& '$(SCRIPTS)/infrastructure/down.ps1'

up: init down
	@& '$(SCRIPTS)/infrastructure/up.ps1'