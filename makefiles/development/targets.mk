atlas-hash:
	@$(call RUN_DEVELOPMENT_SCRIPT,atlas-hash)

uv-lock:
	@$(call RUN_DEVELOPMENT_SCRIPT,uv-lock)

uv-sync:
	@$(call RUN_DEVELOPMENT_SCRIPT,uv-sync)

uv-update: uv-lock uv-sync

.PHONY: \
	atlas-hash \
	uv-lock uv-sync