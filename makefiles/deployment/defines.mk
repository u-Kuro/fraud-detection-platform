# Act Runner
define RUN_ACT_PULL_REQUEST_COMMAND
act pull_request --workflows $(GITHUB_WORKFLOWS_DIRECTORY)/ci-$(1).yaml --eventpath $(GITHUB_EVENTS_DIRECTORY)/pull-request.json
endef
define RUN_ACT_PUSH_COMMAND
act push --workflows $(GITHUB_WORKFLOWS_DIRECTORY)/cd-$(1).yaml
endef