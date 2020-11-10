from enum import auto

from autoname import AutoName


class MessageTag(AutoName):
    """
    https://developers.facebook.com/docs/messenger-platform/send-messages/message-tags
    """

    CONFIRMED_EVENT_UPDATE = auto()
    POST_PURCHASE_UPDATE = auto()
    ACCOUNT_UPDATE = auto()
    HUMAN_AGENT = auto()
