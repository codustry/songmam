from typing import List, Optional, Union

from pydantic import BaseModel, conlist
from songmam.models import ThingWithId
from songmam.models.webhook.events.base import (
    BaseEvent,
    BaseMessaging,
    WithMessaging,
    WithTimestamp,
)
from songmam.models.webhook.events.message.attachment import Attachment


class Sender(ThingWithId):
    user_ref: Optional[str]


class QuickReply(BaseModel):
    """A quick_reply payload is only provided with a text text when the user tap on a Quick Replies button."""

    payload: str


class ReplyTo(BaseModel):
    """"""

    mid: str  # Reference to the text ID that this text is replying to


class Message(BaseModel):
    mid: str  # Message ID
    text: Optional[str] = None  # Text of text
    reply_to: Optional[ReplyTo] = None
    attachments: Optional[List[Attachment]] = None

    @property
    def is_quick_reply(self):
        return False


class MessageWithQuickReply(Message):
    quick_reply: QuickReply

    @property
    def is_quick_reply(self):
        return True

    @property
    def payload(self):
        return self.quick_reply.payload

    def convert_to_no_reply(self):
        return Message(**self.dict(exclude={"quick_replies"}))


class Postback(BaseModel):
    title: str
    payload: str


class MessageMessaging(BaseMessaging, WithTimestamp):
    message: Message


class MessageMessagingWithQuickReply(BaseMessaging, WithTimestamp):
    message: MessageWithQuickReply

    def convert_to_no_reply(self):
        message_without_reply = self.message.convert_to_no_reply()
        return MessageMessaging(
            **self.dict(exclude={"message"}), message=message_without_reply
        )


class UnifiedMessagesEvent(BaseEvent, WithMessaging):
    messaging: conlist(
        Union[MessageMessaging, MessageWithQuickReply], max_items=1, min_items=1
    )

    @property
    def is_quick_reply(self):
        return self.theMessaging.message.is_quick_reply

    @property
    def payload(self):
        if self.is_quick_reply:
            return self.theMessaging.message.payload
        else:
            return None


class MessagesEvent(UnifiedMessagesEvent):
    """
    Without QuickReply
    """

    messaging: conlist(MessageMessaging, max_items=1, min_items=1)


class MessagesEventWithQuickReply(UnifiedMessagesEvent):
    """
    With QuickReply
    """

    messaging: conlist(MessageMessagingWithQuickReply, max_items=1, min_items=1)

    def convert_to_no_reply(self):
        messaging_without_reply = [self.theMessaging.convert_to_no_reply()]
        return MessagesEvent(
            **self.dict(exclude={"messaging"}),
            messaging=messaging_without_reply,
        )
