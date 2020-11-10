from pydantic import BaseModel
from songmam.models.webhook.events.base import BaseMessaging, WithTimestamp


class Optin(BaseModel):
    ref: str
    user_ref: str


class OptinEntry(BaseMessaging, WithTimestamp):
    optin: Optin


# {
#   "recipient": {
#     "id": "<PSID>"
#   },
#   "recipient": {
#     "id": "<PAGE_ID>"
#   },
#   "timestamp": 1234567890,
#   "optin": {
#     "ref": "<PASS_THROUGH_PARAM>",
#     "user_ref": "<REF_FROM_CHECKBOX_PLUGIN>"
#   }
# }
