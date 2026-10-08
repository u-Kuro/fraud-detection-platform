# Image builder
build-infrastructure-image:
	@$(call BUILD_IMAGE,$(INFRASTRUCTURE_DOCKERFILE),$(INFRASTRUCTURE_IMAGE))

# Container runner
infrastructure-up: build-infrastructure-image
	@$(call RUN_INFRASTRUCTURE_TARGET_IN_CONTAINER,infrastructure-container-up)

infrastructure-down: build-infrastructure-image
	@$(call RUN_INFRASTRUCTURE_TARGET_IN_CONTAINER,infrastructure-container-down)

infrastructure-test: build-infrastructure-image
	@$(call RUN_INFRASTRUCTURE_TARGET_IN_CONTAINER,infrastructure-container-validate)

infrastructure-format: build-infrastructure-image
	@$(call RUN_INFRASTRUCTURE_TARGET_IN_CONTAINER,infrastructure-container-format)

# Container scripts
infrastructure-container-init:
	@$(call CONFIGURE_AWS_IN_CONTAINER)
	@$(call RUN_INFRASTRUCTURE_SCRIPT,init)

infrastructure-container-up: infrastructure-container-init infrastructure-container-down
	@$(call RUN_INFRASTRUCTURE_SCRIPT,up)

infrastructure-container-down: infrastructure-container-init
	@$(call RUN_INFRASTRUCTURE_SCRIPT,down)

infrastructure-container-validate: infrastructure-container-init
	@$(call RUN_INFRASTRUCTURE_SCRIPT,validate)

infrastructure-container-format:
	@$(call RUN_INFRASTRUCTURE_SCRIPT,format)

.PHONY: \
	build-infrastructure-image \
	infrastructure-up infrastructure-down \
	infrastructure-test infrastructure-container-format \
	infrastructure-container-init infrastructure-container-up infrastructure-container-down \
	infrastructure-container-validate infrastructure-container-format