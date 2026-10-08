import threading

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

from fraud_detection_platform_shim.modules.environment.slack import slack_environment

slack_app = App(
    token=slack_environment.SLACK_BOT_USER_OAUTH_TOKEN,
    signing_secret=slack_environment.SLACK_SIGNING_SECRET
)

def register_slack_handlers() -> None:
    # These imports are used to register slack handlers
    # noinspection unused-imports
    from fraud_detection_platform_shim.controllers.handlers.slack import ( # noqa: F401
        promotion,
        training
    )

def start_socket_mode() -> None:
    register_slack_handlers()

    handler = SocketModeHandler(
        app=slack_app,
        app_token=slack_environment.SLACK_APP_LEVEL_TOKEN,
    )

    threading.Thread(
        target=handler.start,
        daemon=True,
        name="slack_socket_mode"
    ).start()

def update_message(
    client: WebClient,
    body: dict,
    text_markdown: str
) -> None:
    blocks = [
        block for block in body["message"]["blocks"]
        if block["type"] != "actions"
    ]

    blocks.append({
        "type": "section",
        "text": {"type": "mrkdwn", "text": text_markdown}
    })

    client.chat_update(
        channel=body["channel"]["id"],
        ts=body["message"]["ts"],
        blocks=blocks,
        text=text_markdown,
    )