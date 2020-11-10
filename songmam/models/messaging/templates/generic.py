from typing import List, Literal, Optional

from pydantic import BaseModel, HttpUrl, conlist
from songmam.models.messaging.templates.button import AllButtonTypes


class GenericElement(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/generic#elements
    """

    title: str
    subtitle: Optional[str]
    image_url: Optional[HttpUrl]
    default_action: Optional[
        AllButtonTypes
    ]  # link to url if press on the image that showed
    buttons: Optional[conlist(AllButtonTypes, min_items=1, max_items=3)]


class PayloadGeneric(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/generic
    """

    template_type: str = "generic"
    image_aspect_ratio: Optional[Literal["horizontal", "square"]] = None
    elements: List[GenericElement]
