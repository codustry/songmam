from typing import List, Literal, Optional, Type, Union

from copy import deepcopy
from enum import auto

# from songmam.models.messaging.templates import CompletePayload as Payload_
from autoname import AutoName
from pydantic import (
    BaseModel,
    HttpUrl,
    conlist,
    constr,
    root_validator,
    validator,
)


class BaseButton(BaseModel):
    type: str

    # make optional for default action
    title: Optional[constr(max_length=20)] = None

    def get_default_action(self):
        default_action = deepcopy(self)
        default_action.title = None
        return default_action

    @classmethod
    def create_default_action(cls, *args, **kargs):
        b = cls(**kargs)
        return b.get_default_action()


class URLButton(BaseButton):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/buttons/url
    Updated: 04/07/2020
    """

    type: str = "web_url"
    url: HttpUrl
    webview_height_ratio: Literal["compact", "tall", "full"] = "full"
    messenger_extensions: bool = False
    fallback_url: Optional[HttpUrl]
    webview_share_button: Optional[Literal["hide"]]

    @root_validator
    def fallback_url_should_not_be_specify_if_messenger_extensions_is_false(
        cls, values
    ):
        messenger_extensions, fallback_url = (
            values.get("messenger_extensions"),
            values.get("fallback_url"),
        )
        if fallback_url:
            if not messenger_extensions:
                raise ValueError(
                    "`fallback_url` may only be specified if `messenger_extensions` is true."
                )
        return values


class PostbackButton(BaseButton):
    type: str = "postback"
    payload: str


class CallButton(BaseButton):
    type: str = "phone_number"
    payload: str

    # TODO: https://pypi.org/project/phonenumbers/


class LogInButton(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/send-messages/buttons#login
    """

    type: str = "account_link"
    url: HttpUrl  # Authentication callback URL. Must use HTTPS protocol.


class LogOutButton(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/buttons/logout
    """

    type: str = "account_unlink"


class GameMetadata(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/buttons/game-play#game_metadata
    """

    player_id: Optional[str]
    context_id: Optional[str]


class GamePlayButton(BaseButton):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/buttons/game-play
    """

    type: str = "game_play"
    title: str
    payload: Optional[str]
    game_metadata: Optional[GameMetadata]


# class Button(BaseModel):
#     """
#     https://developers.facebook.com/docs/messenger-platform/reference/buttons/url#properties
#     """
#     type: Literal["web_url", "postback", "phone_number", "account_link", "account_unlink", "game_play"]
#     title: str
#     payload: Optional[str]  # for type : postback / phone_number / game_play
#     url: Optional[HttpUrl]  # for type: web_url / LogIn
#     webview_height_ratio: Optional[Literal["compact", "tall", "full"]]  # for type: web_url
#     messenger_extensions: Optional[bool]  # for type: web_url
#     fallback_url: Optional[HttpUrl]  # for type: web_url
#     webview_share_button: Optional[str]  # for type: web_url
#     game_metadata: Optional[GameMetadata]  # for type : game_play

AllButtonTypes = Union[
    URLButton,
    PostbackButton,
    CallButton,
    LogInButton,
    LogOutButton,
    GamePlayButton,
]


# TODO: Inherit from the CompletePayload?
class PayloadButtonTemplate(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/templates/button
    """

    template_type = "button"
    text: str
    buttons: conlist(
        AllButtonTypes, min_items=1, max_items=3
    )  # Set of 1-3 buttons that appear as call-to-actions.

    @validator("text")
    def title_limit_to_640_characters(cls, v):
        if len(v) > 640:
            raise ValueError("UTF-8-encoded text of up to 640 characters.")
        return v


class ButtonType(AutoName):
    web_url = auto()
    postback = auto()
    phone_number = auto()
    account_link = auto()
    account_unlink = auto()
    game_play = auto()
