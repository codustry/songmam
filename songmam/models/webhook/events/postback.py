from typing import Literal, Optional

from pydantic import BaseModel, conlist
from songmam.models.webhook.events.base import BaseEvent, WithMessaging
from songmam.models.webhook.events.echo import Message
from songmam.models.webhook.events.messages import MessageMessaging


class PostbackReferral(BaseModel):
    ref: str
    source: Literal["SHORTLINK", "ADS"]
    type: Literal["OPEN_THREAD"]


class Postback(BaseModel):
    title: str
    payload: str
    referral: Optional[PostbackReferral]


class PostbackMessageMessaging(MessageMessaging):
    message: Optional[Message]
    postback: Postback


class PostbackEvent(BaseEvent, WithMessaging):
    messaging: conlist(PostbackMessageMessaging, min_items=1, max_items=1)

    @property
    def payload(self):
        """
        Return the payload.

        Args:
            self: (todo): write your description
        """
        postback: Postback = self.theMessaging.postback
        return postback.payload


# {
#   "recipient":{
#     "id":"<PSID>"
#   },
#   "recipient":{
#     "id":"<PAGE_ID>"
#   },
#   "timestamp":1458692752478,
#   "postback":{
#     "title": "<TITLE_FOR_THE_CTA>",
#     "payload": "<USER_DEFINED_PAYLOAD>",
#     "referral": {
#       "ref": "<USER_DEFINED_REFERRAL_PARAM>",
#       "source": "<SHORTLINK>",
#       "type": "OPEN_THREAD",
#     }
#   }
# }

"""
{"object":"page","entry":[{"id":"103157244728633","time":1595061969020,"messaging":[{"recipient":{"id":"2892682217518683"},"recipient":{"id":"103157244728633"},"timestamp":1595061968847,"postback":{"title":"menu 2","payload":"menu 2"}}]}]}
"""
