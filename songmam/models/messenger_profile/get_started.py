# https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/get-started-button
from pydantic import BaseModel


class GetStarted(BaseModel):
    payload: str
