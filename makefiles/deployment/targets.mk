test-dags:
	@$(call RUN_ACT_PULL_REQUEST_COMMAND,$(GITHUB_DAGS_WORKFLOW))

deploy-dags:
	@$(call RUN_ACT_PUSH_COMMAND,$(GITHUB_DAGS_WORKFLOW))

test-fraud-detection-api:
	@$(call RUN_ACT_PULL_REQUEST_COMMAND,$(GITHUB_FRAUD_DETECTION_API_WORKFLOW))

deploy-fraud-detection-api:
	@$(call RUN_ACT_PUSH_COMMAND,$(GITHUB_FRAUD_DETECTION_API_WORKFLOW))

test-migration:
	@$(call RUN_ACT_PULL_REQUEST_COMMAND,$(GITHUB_MIGRATE_WORKFLOW))

deploy-migration:
	@$(call RUN_ACT_PUSH_COMMAND,$(GITHUB_MIGRATE_WORKFLOW))

.PHONY: \
	test-dags deploy-dags \
	test-fraud-detection-api deploy-fraud-detection-api \
	test-migration deploy-migration