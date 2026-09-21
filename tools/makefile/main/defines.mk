# Script Runner
define RUN_SCRIPT
$(SCRIPT_RUNNER) "$(1)/$(SCRIPT_FOLDER)/$(2).$(SCRIPT_EXTENSION)"
endef
define RUN_BASH_SCRIPT
$(SCRIPT_RUNNER) "$(1)/$(2).sh"
endef
define RUN_MAIN_SCRIPT
$(call RUN_SCRIPT,$(MAIN_SCRIPT_DIRECTORY),$(1))
endef

# Script Formatter
define FORMAT_SCRIPT_ARGUMENTS
$(if $(filter $(SHELL_COMMAND), powershell.exe),"-$(1):$(2)","$(2)")
endef

# Docker
define BUILD_IMAGE
$(if $(filter $(IS_INSIDE_FRAUD_DETECTION_PLATFORM_DOCKER),true),,$(call RUN_MAIN_SCRIPT,build-image) $(call FORMAT_SCRIPT_ARGUMENTS,DOCKERFILE,$(1)) $(call FORMAT_SCRIPT_ARGUMENTS,IMAGE,$(2)))
endef
define RUN_TARGET_IN_CONTAINER
$(SCRIPT_RUNNER) "$(1)/run-target.$(SCRIPT_EXTENSION)" $(2) $(3)
endef