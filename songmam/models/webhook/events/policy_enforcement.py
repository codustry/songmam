from pydantic import BaseModel, Field
from songmam.models import ThingWithId


class PolicyEnforcement(BaseModel):
    action: str
    reason: str


class PolicyEnforcementEntry(BaseModel):
    recipitent: ThingWithId
    timestamp: int
    policy_enforcement: PolicyEnforcement = Field(
        None, alias="policy-enforcement"
    )


# {
#   "recipient": {
#     "id": "PAGE_ID"
#   },
#   "timestamp": 1458692752478,
#   "policy-enforcement": {
#     "action": "block",
#     "reason": "The bot violated our Platform Policies (https://developers.facebook.com/policy/#messengerplatform). Common violations include sending out excessive spammy messages or being non-functional."
#   }
# }
