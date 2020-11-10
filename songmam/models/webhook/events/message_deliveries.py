from typing import List, Optional

from pydantic import BaseModel, conlist
from songmam.models.webhook.events.base import (
    BaseEvent,
    BaseMessaging,
    WithMessaging,
    WithTimestamp,
)


class Delivery(BaseModel):
    mids: Optional[List[str]]
    watermark: int


class DeliveriesMessaging(BaseMessaging, WithTimestamp):
    delivery: Delivery


class MessageDeliveriesEvent(BaseEvent, WithMessaging):
    messaging: conlist(DeliveriesMessaging, min_items=1, max_items=1)

    @property
    def mids(self):
        return self.theMessaging.delivery.mids

    @property
    def watermark(self):
        return self.theMessaging.delivery.watermark


# DeliveryEvent = MessageDeliveriesEvent
"""
https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/message-deliveries
"""
