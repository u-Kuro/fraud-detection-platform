from unittest.mock import MagicMock

from fraud_detection_api.services.slack import update_message

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