"""
Payload is final data  form ready to use with request api
"""
from typing import Any, Optional, Union

from enum import auto

from pydantic import BaseModel, conlist
from songmam.models import ThingWithId
from songmam.models.messaging.message_tags import MessageTag
from songmam.models.messaging.messaging_type import MessagingType
from songmam.models.messaging.notification_type import NotificationType
from songmam.models.messaging.sender_action import SenderAction
from songmam.models.messaging.templates import Message
from songmam.models.messaging.templates.button import AllButtonTypes
from songmam.models.send import SendRecipient
from songmam.models.webhook.events.messages import Sender


class CompletePayload(BaseModel):
    recipient: Union[SendRecipient, Sender, ThingWithId]
    template_type: Optional[str] = None
    message: Optional[Message]
    messaging_type: Optional[MessagingType] = MessagingType.RESPONSE
    tag: Optional[MessageTag]
    notification_type: Optional[NotificationType] = NotificationType.REGULAR

    persona_id: Optional[str] = None


class SenderActionPayload(CompletePayload):
    sender_action: SenderAction


class SendingQuickRepliesEntry(CompletePayload):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/buttons/quick-replies
    """

    message: Any
    buttons: conlist(
        AllButtonTypes, max_items=3, min_items=1
    )  # Set of 1-3 buttons that appear as call-to-actions.


from autoname import AutoNameLowercase


class SenderAction(AutoNameLowercase):
    """https://developers.facebook.com/docs/messenger-platform/send-messages/sender-actions"""

    TYPING_ON = auto()
    TYPING_OFF = auto()
    MARK_SEEN = auto()
