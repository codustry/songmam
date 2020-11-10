from typing import Literal, Optional

from pydantic import BaseModel, HttpUrl


class Coordinates(BaseModel):
    lat: float
    long: float


class PayloadOfAttachment(BaseModel):
    url: HttpUrl
    title: Optional[str]
    sticker_id: Optional[int]
    coordinates: Optional[Coordinates]


class Attachment(BaseModel):
    type: Literal[
        "audio", "file", "image", "location", "video", "fallback", "template"
    ]
    payload: PayloadOfAttachment
