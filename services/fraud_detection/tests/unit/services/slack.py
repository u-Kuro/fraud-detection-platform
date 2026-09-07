from unittest.mock import MagicMock

from services.fraud_detection.src.services.slack import update_message

def test_update_message():
    update_message(
        client=MagicMock(),
        body={
            "channel": {
                "id": "value"
            },
            "message": {
                "ts": "value"
            }
        },
        text_markdown="value"
    )