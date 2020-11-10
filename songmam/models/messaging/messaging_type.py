from enum import auto

from autoname import AutoName


class MessagingType(AutoName):
    RESPONSE = auto()
    UPDATE = auto()
    MESSAGE_TAG = auto()
