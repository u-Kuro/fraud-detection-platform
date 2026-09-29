.NOTPARALLEL:

# Main
include makefiles/main/variables.mk
include makefiles/main/defines.mk
# Infrastructure
include makefiles/infrastructure/variables.mk
include makefiles/infrastructure/defines.mk
include makefiles/infrastructure/targets.mk
# Deployment
include makefiles/deployment/variables.mk
include makefiles/deployment/defines.mk
include makefiles/deployment/targets.mk
# Operations
include makefiles/operations/main/variables.mk
# Start pipeline operation
include makefiles/operations/start_pipeline/variables.mk
include makefiles/operations/start_pipeline/defines.mk
include makefiles/operations/start_pipeline/targets.mk
# Development
include makefiles/development/variables.mk
include makefiles/development/defines.mk
include makefiles/development/targets.mk

init: uv-sync

update: atlas-hash uv-update

up: update \
	infrastructure-up \
	deploy-migration \
	deploy-dags \
	start-pipeline

down: infrastructure-down

no-target:
	@$(error Error: no target given, e.g. 'make up')

.PHONY: init up down update no-target
.DEFAULT_GOAL := no-target