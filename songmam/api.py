from typing import List, Literal, Optional, Set, Type, Union

import asyncio
import json
from functools import partial
from inspect import iscoroutine

import httpx
from avajana.bubbling import Bubbling
from furl import furl
from loguru import logger
from songmam.models import ThingWithId
from songmam.models.messaging.message_tags import MessageTag
from songmam.models.messaging.messaging_type import MessagingType
from songmam.models.messaging.notification_type import NotificationType
from songmam.models.messaging.payload import (
    CompletePayload,
    SenderActionPayload,
)
from songmam.models.messaging.quick_replies import QuickReply
from songmam.models.messaging.sender_action import SenderAction
from songmam.models.messaging.templates import (
    AllButtonTypes,
    Message,
    PayloadButtonTemplate,
    PayloadMedia,
    TemplateAttachment,
)
from songmam.models.messaging.templates.generic import (
    GenericElement,
    PayloadGeneric,
)
from songmam.models.messaging.templates.media import MediaElement
from songmam.models.messenger_profile import (
    MenuPerLocale,
    MessengerProfile,
    MessengerProfileProperty,
)
from songmam.models.messenger_profile.persistent_menu import UserPersistentMenu
from songmam.models.page import Page
from songmam.models.persona import (
    AllPerosnasResponse,
    Persona,
    PersonaDeleteResponse,
    PersonaResponse,
    PersonaWithId,
)
from songmam.models.send import SendResponse
from songmam.models.user_profile import UserProfile
from songmam.models.webhook.events.message.attachment import Attachment
from songmam.models.webhook.events.messages import Sender


class MessengerApi:
    access_token: str
    api_version: str = "v8.0"

    def __init__(self, access_token: str, *, auto_avajana: bool = False):
        self.access_token = access_token
        self.auto_avajana = auto_avajana

    @property
    def base_api_furl(self) -> furl:
        furl_url = furl("https://graph.facebook.com/") / self.api_version
        # furl_url.args['access_token'] = self.access_token
        return furl_url

    @property
    def avajana(self) -> Bubbling:
        if not hasattr(self, "_avajana"):
            self._avajana = Bubbling()
        return self._avajana

    @avajana.setter
    def avajana(self, value):
        if isinstance(value, Bubbling):
            self._avajana = value
        else:
            raise ValueError("This needs to be type of Bubbling")

    async def _fetch_page_info(self):
        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token},
        ) as client:
            response = await client.get(f"/me")

        if response.status_code != 200:
            raise Exception(response.text)

        self.page = Page.parse_raw(response.text)

    async def get_user_profile(
        self,
        user: Type[ThingWithId],
        fields: Optional[Set[str]] = None,
    ) -> UserProfile:
        """
        Get user profile using id
        References:
            https://developers.facebook.com/docs/messenger-platform/identity/user-profile
        """
        if fields:
            fields = {
                "id",
                "name",
                "first_name",
                "last_name",
                "profile_pic",
            }

        fields = ",".join(fields)
        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token, "fields": fields},
        ) as client:
            response = await client.get(f"/{user.id}")

        if response.status_code != 200:
            raise Exception(response.text)

        user_profile = UserProfile.parse_raw(response.text)
        return user_profile

    # def get_messenger_code(self, ref=None, image_size=1000):
    #     d = {}
    #     d['type'] = 'standard'
    #     d['image_size'] = image_size
    #     if ref:
    #         d['data'] = {'ref': ref}
    #
    #     r = requests.post(self._api_uri("me/messenger_codes"),
    #                       params={"access_token": self.access_token},
    #                       json=d,
    #                       headers={'Content-type': 'application/json'})
    #     if r.status_code != requests.codes.ok:
    #         raise Exception(r.text)
    #
    #     data = json.loads(r.text)
    #     if 'uri' not in data:
    #         raise ValueError('Could not fetch messener code : GET /' +
    #                          self.api_version + '/me')
    #
    #     return data['uri']

    async def send_native(
        self, payload: Union[CompletePayload], callback=None
    ) -> SendResponse:

        data = payload.json(exclude_none=True)

        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token},
        ) as client:
            response = await client.post(
                "/me/messages",
                data=data,
            )

        if response.status_code != 200:
            raise Exception(response.text)

        if callback is not None:
            callback_output = callback(payload, response)
            if iscoroutine(callback_output):
                await callback

        # if self._after_send is not None:
        #     return_ = self._after_send(payload, response)
        #     if  iscoroutine(return_):
        #         await return_

        return SendResponse.parse_raw(response.text)

    def compose_text(
        self,
        text: str,
        buttons: Optional[Union[AllButtonTypes, List[AllButtonTypes]]] = None,
        attachment: Optional[Attachment] = None,
        quick_replies: Optional[List[QuickReply]] = None,
    ):
        recipient = ThingWithId.create_none()

        if buttons:
            if attachment is not None:
                logger.error(
                    "Only button or attachment could be set at a time. Your attactment will be skip"
                )

            if not isinstance(buttons, list):
                buttons = [buttons]
            payload = CompletePayload(
                recipient=recipient,
                message=Message(
                    attachment=TemplateAttachment(
                        payload=PayloadButtonTemplate(
                            template_type="button", text=text, buttons=buttons
                        )
                    ),
                    quick_replies=quick_replies,
                ),
            )
        elif attachment:
            # todo: verbose if text is specify or add validation to message
            # Exception('{"error":{"message":"(#100) Only one of the text, attachment, and dynamic_text fields can be specified","type":"OAuthException","code":100,"error_subcode":2018191,"fbtrace_id":"A7Y-lr_YqkgZCbTzCfc8iyi"}}')
            payload = CompletePayload(
                recipient=recipient,
                message=Message(
                    attachment=attachment,
                    quick_replies=quick_replies,
                ),
            )
        else:
            payload = CompletePayload(
                recipient=recipient,
                message=Message(text=text, quick_replies=quick_replies),
            )
        return payload

    def send_receipt(self):
        from typing import List, Optional

        from dataclasses import dataclass

        from songmam.models.messaging.quick_replies import QuickReply
        from songmam.models.messaging.templates import (
            Message,
            TemplateAttachment,
        )
        from songmam.models.messaging.templates.receipt import (
            Address,
            Adjustments,
            PayloadReceipt,
            ReceiptElements,
            Summary,
        )

        @dataclass
        class ContentReceipt:
            quick_replies: Optional[List[QuickReply]]
            sharable: Optional[bool]
            recipient_name: str
            merchant_name: Optional[str]
            order_number: str
            currency: str
            payment_method: str  # This can be a custom string, such as, "Visa 1234".
            timestamp: Optional[str]
            elements: Optional[List[ReceiptElements]]
            address: Optional[Address]
            summary: Summary
            adjustments: Optional[List[Adjustments]]

            @property
            def message(self):
                message = Message()

                if self.elements:
                    payload = PayloadReceipt(
                        template_type="receipt",
                        recipient_name=self.recipient_name,
                        order_number=self.order_number,
                        currency=self.currency,
                        payment_method=self.payment_method,  # This can be a custom string, such as, "Visa 1234".
                        summary=self.summary,
                    )
                    payload.sharable = self.sharable
                    payload.merchant_name = self.merchant_name
                    payload.timestamp = self.timestamp
                    payload.elements = self.elements
                    payload.address = self.address
                    payload.adjustments = self.adjustments
                    message.attachment = TemplateAttachment(payload=payload)
                if self.quick_replies:
                    message.quick_replies = self.quick_replies

                return message

        raise NotImplementedError

    def compose_media(
        self,
        media_element: MediaElement,
        media_sharable: Optional[bool] = None,
        quick_replies: Optional[List[QuickReply]] = None,
    ):
        recipient = ThingWithId.create_none()
        payload = CompletePayload(
            recipient=recipient,
            message=Message(
                attachment=TemplateAttachment(
                    payload=PayloadMedia(
                        elements=[media_element],
                        sharable=media_sharable,
                    )
                ),
                quick_replies=quick_replies,
            ),
        )
        return payload

    def compose_generic(
        self,
        generic_elements: Union[GenericElement, List[GenericElement]],
        image_aspect_ratio: Literal["horizontal", "square"] = "square",
        quick_replies: Optional[List[QuickReply]] = None,
    ):
        recipient = ThingWithId.create_none()
        if not isinstance(generic_elements, list):
            generic_elements = [generic_elements]

        payload = CompletePayload(
            recipient=recipient,
            message=Message(
                attachment=TemplateAttachment(
                    payload=PayloadGeneric(
                        elements=generic_elements,
                        image_aspect_ratio=image_aspect_ratio,
                    )
                ),
                quick_replies=quick_replies,
            ),
        )
        return payload

    def rehydrate_payload(
        self,
        payload: CompletePayload,
        recipient: Union[Sender, str],
        persona_id: Optional[str] = None,
        messaging_type: Optional[MessagingType] = MessagingType.RESPONSE,
        tag: Optional[MessageTag] = None,
        notification_type: Optional[
            NotificationType
        ] = NotificationType.REGULAR,
    ):
        if isinstance(recipient, str):
            recipient = Sender(id=recipient)

        payload.recipient = recipient
        payload.persona_id = persona_id
        payload.messaging_type = messaging_type
        payload.tag = tag
        payload.notification_type = notification_type
        return payload

    async def send(
        self,
        recipient: Union[Sender, str],
        text: Optional[str] = None,
        *,
        attachment: Optional[Attachment] = None,
        buttons: Optional[Union[AllButtonTypes, List[AllButtonTypes]]] = None,
        quick_replies: Optional[Union[QuickReply, List[QuickReply]]] = None,
        generic_elements: Optional[
            Union[GenericElement, List[GenericElement]]
        ] = None,
        image_aspect_ratio: Optional[Literal["horizontal", "square"]] = None,
        media_element: Optional[MediaElement] = None,
        media_sharable: Optional[bool] = None,
        persona_id: Optional[str] = None,
        messaging_type: Optional[MessagingType] = MessagingType.RESPONSE,
        tag: Optional[MessageTag] = None,
        notification_type: Optional[
            NotificationType
        ] = NotificationType.REGULAR,
        callback: Optional[callable] = None,
        auto_avajana: Optional[bool] = None,
        emu_type: bool = False,
    ):
        if auto_avajana is None:
            auto_avajana = self.auto_avajana
        if isinstance(recipient, str):
            recipient = Sender(id=recipient)
        if text and auto_avajana:
            typing_fn = partial(self.typing_on, recipient)
            stop_fn = partial(self.typing_off, recipient)
            await self.avajana.act_typing(text, typing_fn, stop_fn)

        if isinstance(quick_replies, QuickReply):
            quick_replies = [quick_replies]

        if generic_elements:
            payload = self.compose_generic(
                generic_elements=generic_elements,
                image_aspect_ratio=image_aspect_ratio,
                quick_replies=quick_replies,
            )
        elif media_element:
            payload = self.compose_media(
                media_element=media_element,
                media_sharable=media_sharable,
                quick_replies=quick_replies,
            )
        else:
            payload = self.compose_text(
                text=text,
                buttons=buttons,
                quick_replies=quick_replies,
                attachment=attachment,
            )

        payload = self.rehydrate_payload(
            payload=payload,
            recipient=recipient,
            persona_id=persona_id,
            messaging_type=messaging_type,
            tag=tag,
            notification_type=notification_type,
        )

        return await self.send_native(payload, callback=callback)

    # async def reply(self, message_to_reply_to: MessageEvent, text, *, quick_replies=None, metadata=None,
    #                 notification_type=None, tag: Optional[MessageTag] = None, callback: Optional[callable] = None):
    #
    #     if self.prevent_repeated_reply:
    #         message_id = message_to_reply_to.entry.theMessaging.text.mid
    #         if message_id not in self.reply_cache:
    #             # good to go
    #             self.reply_cache.set(message_id, True)
    #         else:
    #             logger.warning("Songmum prevented a text from being reply to the same entry multiple times.")
    #             logger.warning(message_to_reply_to)
    #             return
    #
    #     return await self.send_native(
    #         CompletePayload(
    #             recipient=message_to_reply_to.sender,
    #             text=text.text
    #         ),
    #         callback=callback
    #     )

    async def typing_on(
        self,
        recipient: Union[Sender, str],
    ):
        if isinstance(recipient, str):
            recipient = Sender(id=recipient)

        payload = SenderActionPayload(
            recipient=recipient, sender_action=SenderAction.TYPING_ON
        )

        return await self.send_native(payload)

    async def typing_off(
        self,
        recipient: Union[Sender, str],
    ):
        if isinstance(recipient, str):
            recipient = Sender(id=recipient)

        payload = SenderActionPayload(
            recipient=recipient, sender_action=SenderAction.TYPING_OFF
        )

        return await self.send_native(payload)

    async def mark_seen(self, recipient: Type[ThingWithId]):
        payload = SenderActionPayload(
            recipient=recipient, sender_action=SenderAction.MARK_SEEN
        )

        return await self.send_native(payload)

    async def typing_for(
        self,
        seconds: float,
        recipient: Union[Sender, str],
        prepause_seconds: float = 0.0,
        postpause_seconds: float = 0.0,
    ):
        await asyncio.sleep(prepause_seconds)
        await self.typing_on(recipient)
        await asyncio.sleep(seconds)
        await self.typing_off(recipient)
        await asyncio.sleep(postpause_seconds)

    """
    messenger profile (see https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api)
    """

    async def set_messenger_profile(self, data: MessengerProfile):

        data = data.json(exclude_none=True)
        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token},
        ) as client:
            response = await client.post(
                "/me/messenger_profile",
                data=data,
            )

        if response.status_code != 200:
            raise Exception(response.text)

    async def delete_messenger_profile(
        self, properties: Set[MessengerProfileProperty]
    ):
        data = json.dumps({"fields": [p.value for p in properties]})
        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token},
        ) as client:
            response = await client.request(
                "DELETE",
                "/me/messenger_profile",
                data=data,
            )

        if response.status_code != 200:
            raise Exception(response.text)

    """
    Custom User Settings
    """

    async def get_user_settings(self, user_id: str):

        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token, "psid": user_id},
        ) as client:
            response = await client.get(
                "me/custom_user_settings",
            )

        if response.status_code != 200:
            raise Exception(response.text)

        # TODO: create object for this GET Request
        #  https://developers.facebook.com/docs/messenger-platform/send-messages/persistent-menu
        return response.json()

    async def set_user_menu(
        self, user: Union[str, Type[ThingWithId]], menus: List[MenuPerLocale]
    ):
        if isinstance(user, str):
            user = ThingWithId(id=user)

        if isinstance(menus, MenuPerLocale):
            menus = [menus]

        data = UserPersistentMenu(psid=user.id, persistent_menu=menus).json()

        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token},
        ) as client:
            response = await client.post("me/custom_user_settings", data=data)

        if response.status_code != 200:
            raise Exception(response.text)

    async def delete_user_menu(self, user_id: str):
        params = {
            "access_token": self.access_token,
            "psid": user_id,
            "params": '["persistent_menu"]',
        }

        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params=params,
        ) as client:
            response = await client.delete(
                "me/custom_user_settings",
            )

        if response.status_code != 200:
            raise Exception(response.text)

        return response.json()

    async def create_persona(self, persona: Persona) -> PersonaResponse:
        data = persona.json()

        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token},
        ) as client:
            response = await client.post(
                "/me/personas",
                data=data,
            )

        if response.status_code != 200:
            raise Exception(response.text)

        return PersonaResponse.parse_raw(response.text)

    async def get_persona(self, id):

        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token},
        ) as client:
            response = await client.get(
                f"/{id}",
            )

        if response.status_code != 200:
            raise Exception(response.text)

        return PersonaWithId.parse_raw(response.text)

    async def get_all_personas(self) -> List[PersonaWithId]:

        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token},
        ) as client:
            response = await client.get(
                f"/me/personas",
            )

        if response.status_code != 200:
            raise Exception(response.text)

        response = AllPerosnasResponse.parse_raw(response.text)

        # There might be a need to implement paging in future
        # Note: https://developers.facebook.com/docs/graph-api/using-graph-api/#cursors

        return response.data

    async def delete_persona(self, id):

        async with httpx.AsyncClient(
            base_url=self.base_api_furl.url,
            headers={"Content-type": "application/json"},
            params={"access_token": self.access_token},
        ) as client:
            response = await client.delete(
                f"/{id}",
            )

        if response.status_code != 200:
            raise Exception(response.text)

        return PersonaDeleteResponse.parse_raw(response.text)
