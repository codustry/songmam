from typing import Optional

from fastapi import FastAPI
from pydantic import BaseSettings

from songmam import WebhookHandler, MessengerApi
from songmam.models.webhook import MessagesEvent

app = FastAPI(
    title="echo chan"
)


class FacebookSettings(BaseSettings):
    FACEBOOK_APP_SECRET: Optional[str] = None
    FACEBOOK_PAGE_ACCESS_TOKEN: str
    FACEBOOK_PAGE_VERIFY_TOKEN: Optional[str] = None

    def create_messenger_api(self):
        return MessengerApi(
            access_token=self.FACEBOOK_PAGE_ACCESS_TOKEN,
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = FacebookSettings()

handler = WebhookHandler(
    app, app_secret=settings.FACEBOOK_APP_SECRET, verify_token=settings.FACEBOOK_PAGE_VERIFY_TOKEN
)

api = settings.create_messenger_api()


@handler.add(MessagesEvent)
async def handle_message(event: MessagesEvent, *args, **kwargs):
    """
    echo back message
    """
    await api.send(event.theMessaging.sender, event.theMessaging.message.text)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="debug"
    )

