# Image builder
build-infrastructure-image:
	@$(call BUILD_IMAGE,$(INFRASTRUCTURE_DOCKERFILE),$(INFRASTRUCTURE_IMAGE))

# Container runner
infrastructure-up: build-infrastructure-image infrastructure-down
	@$(call RUN_INFRASTRUCTURE_TARGET_IN_CONTAINER,infrastructure-container-up)
infrastructure-down: build-infrastructure-image
	@$(call RUN_INFRASTRUCTURE_TARGET_IN_CONTAINER,infrastructure-container-down)

# Container scripts
infrastructure-container-init:
	@$(call RUN_INFRASTRUCTURE_SCRIPT,init)

infrastructure-container-up: infrastructure-container-init infrastructure-container-down
	@$(call RUN_INFRASTRUCTURE_SCRIPT,up)

infrastructure-container-down: infrastructure-container-init
	@$(call RUN_INFRASTRUCTURE_SCRIPT,down)

.PHONY: build-infrastructure-image \
	infrastructure-up infrastructure-down \
	infrastructure-container-init infrastructure-container-up infrastructure-container-down