from typing import Literal, Optional, Union

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
        """
        Returns the default action.

        Args:
            self: (todo): write your description
        """
        default_action = deepcopy(self)
        default_action.title = None
        return default_action

    @classmethod
    def create_default_action(cls, *args, **kargs):
        """
        Creates an instance.

        Args:
            cls: (callable): write your description
            kargs: (todo): write your description
        """
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
        """
        Determine if the url should be not be used.

        Args:
            cls: (todo): write your description
            values: (dict): write your description
        """
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
        """
        Convert a limit string to the first.

        Args:
            cls: (todo): write your description
            v: (todo): write your description
        """
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
