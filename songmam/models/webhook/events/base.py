from pydantic import BaseModel, conlist
from songmam.models import ThingWithId


class BaseMessaging(BaseModel):
    sender: ThingWithId
    recipient: ThingWithId


class WithTimestamp(BaseModel):
    timestamp: int


class BaseEvent(BaseModel):
    id: str
    time: int


class WithMessaging(BaseModel):
    messaging: conlist(BaseMessaging, min_items=1, max_items=1)

    @property
    def theMessaging(self):
        return self.messaging[0]

    @property
    def sender(self):
        return self.theMessaging.sender

    @property
    def recipient(self):
        return self.theMessaging.recipient
