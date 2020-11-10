# https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/greeting

from pydantic import validator
from songmam.models.locale import ThingWithLocale


class GreetingPerLocale(ThingWithLocale):
    text: str  # Text Could be Personalized e.g. "Hello {{user_first_name}}!"

    @validator("text")
    def char_limit_to_160(cls, value):
        if len(value) > 160:
            raise ValueError("Must be in UTF-8. 160 character limit.")
        return value
