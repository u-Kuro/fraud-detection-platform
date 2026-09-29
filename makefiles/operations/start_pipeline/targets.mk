# Image builder
build-start-pipeline-image:
	@$(call BUILD_IMAGE,$(START_PIPELINE_DOCKERFILE),$(START_PIPELINE_IMAGE))

# Container runner
start-pipeline: build-start-pipeline-image
	@$(call RUN_START_PIPELINE_TARGET_IN_CONTAINER,start-pipeline-container)

# Container scripts
start-pipeline-container: build-start-pipeline-image
	@$(call CONFIGURE_AWS_IN_CONTAINER)
	@$(call RUN_START_PIPELINE_SCRIPT,start-pipeline)

.PHONY: \
	build-start-pipeline-image \
	start-pipeline \
	start-pipeline-container