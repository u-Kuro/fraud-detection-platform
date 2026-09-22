from services_shared.src.services.idempotency import IdempotencyStore

slack_action_store = IdempotencyStore(ttl=10.0)