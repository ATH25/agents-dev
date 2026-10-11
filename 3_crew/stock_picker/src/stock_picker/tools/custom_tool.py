import os

import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class PushNotificationInput(BaseModel):
    """Input schema for the Pushover push notification tool."""

    message: str = Field(
        ...,
        description=(
            "A 1-3 sentence investment-selection summary including the company name, "
            "ticker symbol, and primary reason for selection."
        ),
    )


class PushNotificationTool(BaseTool):
    name: str = "send_push_notification"
    description: str = (
        "Sends the final investment-selection decision to the user via the Pushover "
        "push notification service. Call this only after the best company has been selected."
    )
    args_schema: type[BaseModel] = PushNotificationInput

    def _run(self, message: str) -> str:
        token = os.environ["PUSHOVER_TOKEN"]
        user = os.environ["PUSHOVER_USER"]

        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={"token": token, "user": user, "message": message},
            timeout=10,
        )

        if not response.ok:
            raise RuntimeError(
                f"Pushover notification failed with status {response.status_code}."
            )

        return "Push notification sent successfully."


send_push_notification = PushNotificationTool()
