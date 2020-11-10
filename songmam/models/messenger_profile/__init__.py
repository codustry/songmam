from typing import List, Optional

from enum import auto

from autoname import AutoName
from pydantic import BaseModel, HttpUrl
from songmam.models.messenger_profile.get_started import GetStarted
from songmam.models.messenger_profile.greeting import GreetingPerLocale
from songmam.models.messenger_profile.ice_breakers import IceBreaker
from songmam.models.messenger_profile.persistent_menu import MenuPerLocale


class MessengerProfileProperty(AutoName):
    get_started = auto()
    greeting = auto()
    ice_breakers = auto()
    persistent_menu = auto()
    whitelisted_domains = auto()
    account_linking_url = auto()


class MessengerProfile(BaseModel):
    get_started: Optional[GetStarted]
    greeting: Optional[List[GreetingPerLocale]]
    ice_breakers: Optional[List[IceBreaker]]
    persistent_menu: Optional[List[MenuPerLocale]]
    whitelisted_domains: Optional[List[HttpUrl]]
    account_linking_url: Optional[HttpUrl]
