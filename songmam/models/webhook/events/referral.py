from typing import Literal, Optional

from pydantic import BaseModel, conlist
from songmam.models.webhook.events.base import (
    BaseEvent,
    BaseMessaging,
    WithMessaging,
    WithTimestamp,
)


class Referral(BaseModel):
    ref: str
    source: Literal[
        "MESSENGER_CODE",
        "DISCOVER_TAB",
        "ADS",
        "SHORTLINK",
        "CUSTOMER_CHAT_PLUGIN",
    ]
    type: str
    ad_id: Optional[str]
    referer_uri: Optional[str]


class ReferralMessaging(BaseMessaging, WithTimestamp):
    referral: Referral

    def __getattr__(self, item):
        """
        Return the value from an item

        Args:
            self: (todo): write your description
            item: (str): write your description
        """
        return getattr(self.referral, item)


class MessagingReferralEvent(BaseEvent, WithMessaging):
    messaging: conlist(ReferralMessaging, min_items=1, max_items=1)

    @property
    def ref(self):
        """
        : return the reference

        Args:
            self: (todo): write your description
        """
        return self.theMessaging.ref


# {
#     "recipient": {
#         "id": "<PSID>"
#     },
#     "recipient": {
#         "id": "<PAGE_ID>"
#     },
#     "timestamp": 1458692752478,
#     "referral": {
#                     "ref": < REF_DATA_PASSED_IN_M.ME_PARAM >,
#     "source": "SHORTLINK",
#     "type": "OPEN_THREAD",
# }
# }
