from airflow.providers.slack.hooks.slack import SlackHook
from airflow.sdk import Context
from slack_sdk import WebClient

from dags.shared.modules.configs.slack import SlackConfig
from dags.shared.modules.schemas.airflow import TaskContext

slack_client: WebClient = SlackHook(slack_conn_id=SlackConfig.SLACK_CONNECTION_ID()).client

def slack_failure_alert(context: Context):
    context = TaskContext(context)
    ti = context.task_instance

    header = (
        f"DAG: `{ti.dag_id}`\n\n"
        f"• *Task:* `{ti.task_id}`\n"
        f"• *Run:* `{ti.run_id}`\n"
        f"• *Error:*\n"
    )
    footer = f"\n\n<{ti.log_url}|View Workflow Run>"
    fence = "```"

    # Slack's section block text limits upto 3000 chars
    limit = 3000 - len(header) - len(footer) - 2 * len(fence)

    error = (
        (str(context.exception or "") or "N/A")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace(fence, "'''")
    )
    if len(error) > limit:
        error = error[: max(limit - 1, 0)] + "…"

    slack_client.chat_postMessage(
        channel=SlackConfig.SLACK_CHANNEL_ID(),
        blocks=create_blocks(
            title="⚠️ Task Failed",
            body=f"{header}{fence}{error}{fence}{footer}",
        ),
    )

def create_blocks(title: str, body: str, buttons: list[dict] | None = None) -> list[dict]:
    blocks: list[dict] = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": title
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": body
            }
        },
    ]
    if buttons:
        blocks.append({
            "type": "actions",
            "elements": buttons
        })
    return blocks