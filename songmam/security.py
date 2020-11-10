from typing import Dict, Optional

import base64
import hashlib
import hmac
import json
import re

import arrow
from pydantic import conint


def base64_url_decode(inp) -> bytes:
    """
    Decode base64 - 64 string.

    Args:
        inp: (str): write your description
    """
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "=" * padding_factor
    return base64.b64decode(inp.translate(dict(zip(map(ord, "-_"), "+/"))))


RequestContent = Dict


def verify_signed_request(
    signed_request,
    app_secret,
    acceptable_freshness_sec: Optional[conint(ge=0)] = None,
) -> Optional[RequestContent]:
    """
    Verify Signed Request from Context object retrieves from webview, frontend
    https://developers.facebook.com/docs/messenger-platform/webview/context

    fork from https://gist.github.com/adrienjoly/1373945/0434b4207a268bdd9cbd7d45ac22ec33dfaad199
    """
    encoded_signature, payload = signed_request.split(".")

    signature = base64_url_decode(encoded_signature)
    request_content = json.loads(base64_url_decode(payload))
    issued_at = arrow.get(request_content["issued_at"])

    if request_content.get("algorithm").upper() != "HMAC-SHA256":
        raise NotImplementedError("Unknown algorithm")
    elif (
        acceptable_freshness_sec
        and issued_at.shift(seconds=acceptable_freshness_sec) < arrow.utcnow()
    ):
        raise Exception(
            f"This signed request was too old. It was issue at {issued_at.format()}"
        )
    else:
        calculated_signature = hmac.new(
            str.encode(app_secret), str.encode(payload), hashlib.sha256
        ).digest()

    if signature != calculated_signature:
        return None
    else:
        return request_content


pattern = r"(.+)\.(.+)"
signed_request_regex = re.compile(pattern)


class SignedRequest(str):
    @classmethod
    def __get_validators__(cls):
        """
        Return a list of validators.

        Args:
            cls: (todo): write your description
        """
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        """
        Modify schema schema.

        Args:
            cls: (todo): write your description
            field_schema: (todo): write your description
        """
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
        field_schema.update(
            # simplified regex here for brevity, see the wikipedia link above
            pattern=pattern,
            # some example postcodes
            examples=[
                "kyYc0BUmhpqnlzGgf8_FgVMISpiAqo9TRs1Z3xSIX7w.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvbW11bml0eV9pZCI6bnVsbCwiaXNzdWVkX2F0IjoxNjAyMTM2OTE0LCJtZXRhZGF0YSI6bnVsbCwicGFnZV9pZCI6NTc0MTg1MzM2NTk1NjczLCJwc2lkIjoiMzE0OTE1OTI0ODUzNzIxMiIsInRocmVhZF9wYXJ0aWNpcGFudF9pZHMiOm51bGwsInRocmVhZF90eXBlIjoiVVNFUl9UT19QQUdFIiwidGlkIjoiMzE0OTE1OTI0ODUzNzIxMiJ9"
            ],
        )

    @classmethod
    def validate(cls, v):
        """
        Validate a request.

        Args:
            cls: (callable): write your description
            v: (array): write your description
        """
        if not isinstance(v, str):
            raise TypeError("string required")
        m = signed_request_regex.fullmatch(v)
        if not m:
            raise ValueError("invalid signed request format")
        # you could also return a string here which would mean model.post_code
        # would be a string, pydantic won't care but you could end up with some
        # confusion since the value's type won't match the type annotation
        # exactly
        return cls(v)

    def __repr__(self):
        """
        Return a repr representation of a repr__.

        Args:
            self: (todo): write your description
        """
        return f"SignedRequest({super().__repr__()})"

    def verify(
        self,
        app_secret,
        acceptable_freshness_sec: Optional[conint(ge=0)] = None,
    ) -> Optional[RequestContent]:
        """
        Verifies a signed signed request.

        Args:
            self: (todo): write your description
            app_secret: (str): write your description
            acceptable_freshness_sec: (str): write your description
            Optional: (todo): write your description
            conint: (str): write your description
            ge: (str): write your description
        """
        return verify_signed_request(self, app_secret, acceptable_freshness_sec)


def verify_webhook_body(signature, app_secret, body):
    """
    https://developers.facebook.com/docs/messenger-platform/webhook#security
    """
    # signature = request.headers["X-Hub-Signature"]
    assert len(signature) == 45
    assert signature.startswith("sha1=")
    signature = signature[5:]

    # body = await request.body()
    expected_signature = hmac.new(
        str.encode(app_secret), body, hashlib.sha1
    ).hexdigest()

    if expected_signature != signature:
        return False

    return True
