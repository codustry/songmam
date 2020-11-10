"""
    https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/ice-breakers
    """
from pydantic import BaseModel


class IceBreaker(BaseModel):
    question: str
    payload: str
