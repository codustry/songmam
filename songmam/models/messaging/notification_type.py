from enum import auto

from autoname import AutoName


class NotificationType(AutoName):
    REGULAR = auto()
    SILENT_PUSH = auto()
    NO_PUSH = auto()
