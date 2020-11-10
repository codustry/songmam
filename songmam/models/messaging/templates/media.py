from typing import Literal, Optional

from pydantic import BaseModel, conlist
from songmam.models.messaging.templates.button import AllButtonTypes


class MediaElement(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/media#elements
    """

    media_type: Optional[Literal["image", "video"]]
    attachment_id: Optional[str]  # Cannot be used if url is set.
    url: Optional[
        str
    ]  # Cannot be used if attachment_id is set. || have to be image / vids in facebook url
    buttons: Optional[
        conlist(AllButtonTypes, min_items=1, max_items=3)
    ]  # A maximum of 1 button is supported.


class PayloadMedia(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/media#payload
    """

    template_type: Literal["media"] = "media"
    elements: conlist(MediaElement, min_items=1, max_items=1)
    sharable: Optional[bool]
