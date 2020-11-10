from enum import auto

from autoname import AutoNameLowercase


class SenderAction(AutoNameLowercase):
    """https://developers.facebook.com/docs/messenger-platform/send-messages/sender-actions"""

    TYPING_ON = auto()
    TYPING_OFF = auto()
    MARK_SEEN = auto()
