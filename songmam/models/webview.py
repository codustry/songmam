from enum import auto

from autoname import AutoNameUppercase
from pydantic import BaseModel
from pydantic.types import conint
from songmam.security import SignedRequest

# type
Second = conint(ge=0)


class ThreadType(AutoNameUppercase):
    user_to_page = auto()
    user_to_user = auto()
    group = auto()


class SignedRequestContent(BaseModel):
    """
    This class property was created based on a real object. See test for ref.

    # WTF, This is not the same structure as the actual object
    https://developers.facebook.com/docs/reference/login/signed-request
    """

    # code: Optinal[str]
    algorithm: str
    issued_at: int
    # user_id: str
    page_id: str
    psid: str
    thread_type: ThreadType
    tid: str
    # oauth_token
    # expires
    # app_data


class Context(BaseModel):
    """
    https://developers.facebook.com/docs/messenger-platform/reference/messenger-extensions-sdk/getContext
    """

    thread_type: ThreadType
    tid: str
    psid: str
    signed_request: SignedRequest
