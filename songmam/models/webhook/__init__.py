from typing import List, Union

from loguru import logger
from pydantic import BaseModel, validator
from songmam.models.webhook.events import *


class Webhook(BaseModel):
    """An object contains one or more events
    https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/#payload
    """

    object: str
    entry: List[
        Union[
            MessagingReferralEvent,
            MessageReadsEvent,
            MessagesEventWithQuickReply,
            MessagesEvent,
            MessageDeliveriesEvent,
            PostbackEvent,
        ]
    ]

    @validator("object")
    def object_equal_page(cls, v):
        if v != "page":
            error_msg = "only support page subscription"
            logger.error(error_msg)
            raise ValueError(error_msg)
        return v
