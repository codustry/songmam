from typing import Literal, Optional, Union

from pydantic import BaseModel, HttpUrl


class QuickReply(BaseModel):
    content_type: Literal[
        "text", "location", "user_phone_number", "user_email"
    ] = "text"
    title: Optional[str]  # Required if content_type is 'text'
    payload: Optional[Union[str, int]]  # "payload":"<POSTBACK_PAYLOAD>"
    image_url: Optional[HttpUrl]  # Required if title is an empty string.
