from typing import Optional

from pydantic import BaseModel, HttpUrl
from songmam.models.locale import Locale


class UserProfile(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/identity/user-profile
    """

    id: str
    name: str
    first_name: str
    last_name: str
    profile_pic: HttpUrl
    locale: Optional[Locale]
    timezone: Optional[int]
    gender: Optional[str]  # TODO: to be changed to `literal`
