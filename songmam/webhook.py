from typing import Awaitable, Callable, List, Optional, Union

import asyncio
import re

from fastapi import APIRouter, FastAPI, Header, Query, Request
from fastapi.responses import PlainTextResponse
from loguru import logger
from moshimoshi import moshi
from parse import parse
from path import Path
from pydantic import ValidationError
from songmam.models.webhook import MessagesEventWithQuickReply, Webhook
from songmam.models.webhook.events.messages import MessagesEvent
from songmam.models.webhook.events.postback import PostbackEvent
from songmam.security import verify_webhook_body


class WebhookHandler:
    verify_token: Optional[str] = None
    app_secret: Optional[str] = None
    uncaught_postback_handler: Optional[Callable] = None

    def __init__(
        self,
        app: Union[FastAPI, APIRouter],
        path="/webhook",
        *,
        app_secret: Optional[str] = None,
        dynamic_import=True,
        verify_token: Optional[str] = None,
        auto_mark_as_seen: bool = True,
    ):
        self._post_webhook_handlers = {}
        self._pre_webhook_handlers = {}
        self.app = app
        self.verify_token = verify_token
        self.app_secret = app_secret
        self.path = path
        self.dynamic_import = dynamic_import

        if self.verify_token:

            @app.get(path, response_class=PlainTextResponse)
            async def check_token(
                request: Request,
                mode: str = Query(..., alias="hub.mode"),
                verify_token: str = Query(..., alias="hub.verify_token"),
                challenge: str = Query(..., alias="hub.challenge"),
            ):
                """
                https://developers.facebook.com/docs/messenger-platform/getting-started/webhook-setup
                """
                if mode == "subscribe" and verify_token == self.verify_token:
                    return challenge
                else:
                    return PlainTextResponse(
                        "Bad Verification Token", status_code=403
                    )

        else:

            @app.get(path, response_class=PlainTextResponse)
            async def check_token(
                request: Request,
                mode: str = Query(..., alias="hub.mode"),
                verify_token: str = Query(..., alias="hub.verify_token"),
                challenge: str = Query(..., alias="hub.challenge"),
            ):
                """
                https://developers.facebook.com/docs/messenger-platform/getting-started/webhook-setup
                """
                logger.warning(
                    "Without verify token supplied, you and your sever might confused about fb app."
                )
                return challenge

        @app.post(path)
        async def handle_entry(
            request: Request,
            signature: str = Header(..., alias="X-Hub-Signature"),
        ):
            body = await request.body()

            if self.app_secret:
                if verify_webhook_body(signature, self.app_secret, body):
                    logger.debug("verify webhook success")
                else:
                    logger.error("fail to verify app secret")
            else:
                logger.warning(
                    "Without app secret supplied, The server will not be able to identity the integrety of callback."
                )

            try:
                webhook = Webhook.parse_raw(body)
                await self.handle_webhook(webhook, request=request)
            except ValidationError as e:
                logger.error("Cannot parse webhook")
                logger.error("Body is {}", body)
            return "ok"

    # these are set by decorators or the 'set_webhook_handler' method
    _webhook_handlers = {}

    _quick_reply_callbacks = {}
    _button_callbacks = {}
    _delivered_callbacks = {}

    _quick_reply_callbacks_key_regex = {}
    _button_callbacks_key_regex = {}
    _delivered_callbacks_key_regex = {}

    async def handle_webhook(self, webhook: Webhook, *args, **kwargs):
        for event in webhook.entry:
            event_type = type(event)

            # quick_replies raw input escape
            if event_type is MessagesEventWithQuickReply:
                if event.payload == "#raw_input":
                    event = event.convert_to_no_reply()
                    event_type = MessagesEvent
                elif event.payload.startswith("#input_as"):
                    the_parsed = parse("#input_as#{text}", event.payload)
                    event = event.convert_to_no_reply()
                    event.theMessaging.message.text = the_parsed.text
                    event_type = MessagesEvent

            # Unconditional handlers
            handler = self._webhook_handlers.get(event_type)
            if handler:
                asyncio.create_task(handler(event, *args, **kwargs))
            else:
                if not self.dynamic_import and event_type is PostbackEvent:
                    logger.warning(
                        "there's no handler for this event type, {}",
                        str(event_type),
                    )

            # Dynamic handlers
            if event_type is MessagesEventWithQuickReply:
                if self.dynamic_import:
                    asyncio.create_task(
                        self.call_dynamic_function(*args, event=event, **kwargs)
                    )
                else:
                    matched_callbacks = self.get_quick_reply_callbacks(event)
                    for callback in matched_callbacks:
                        asyncio.create_task(callback(event, *args, **kwargs))
            elif event_type is PostbackEvent:
                if self.dynamic_import:
                    asyncio.create_task(
                        self.call_dynamic_function(*args, event=event, **kwargs)
                    )
                matched_callbacks = self.get_postback_callbacks(event)
                for callback in matched_callbacks:
                    asyncio.create_task(callback(event, *args, **kwargs))

    async def call_dynamic_function(
        self,
        *args,
        event: Union[MessagesEventWithQuickReply, PostbackEvent],
        **kwargs,
    ):
        payload = event.payload
        kwargs["event"] = event
        if self.uncaught_postback_handler:
            await moshi.moshi(
                payload,
                *args,
                fallback=self.uncaught_postback_handler,
                **kwargs,
            )
        else:
            try:
                await moshi.moshi(payload, *args, **kwargs)
            except ModuleNotFoundError as e:
                import os

                logger.debug("This is cwd, {}", os.getcwd())
                logger.exception("Verbose about exception")
                logger.warning(
                    "You could add `uncaught_postback_handler` to caught this '{}' payload",
                    event.payload,
                )

    def add_pre(self, entry_type):
        """
        Add an unconditional event handler
        """

        def decorator(func):
            self._pre_webhook_handlers[entry_type] = func
            # if isinstance(text, (list, tuple)):
            #     for it in text:
            #         self.__add_handler(func, entry, text=it)
            # else:
            #     self.__add_handler(func, entry, text=text)

            return func

        return decorator

    def add(
        self,
        event_type,
        # skipQuickReply:Optional[bool]=None
    ):
        """
        Add an event handler
        """

        # conditions = tuple(skipQuickReply)
        # didPassSomeCondition = any((x is None for x in conditions))
        # spaces = [(event_type), ]
        # for con in conditions:
        #     if get_args(con) is bool:
        #         if con is None:
        #             spaces.append((True, False))
        #         else:
        #             spaces.append(tuple(con))

        def decorator(func):
            # for condition in product(*spaces):
            self._webhook_handlers[event_type] = func

            # if isinstance(text, (list, tuple)):
            #     for it in text:
            #         self.__add_handler(func, entry, text=it)
            # else:
            #     self.__add_handler(func, entry, text=text)

            return func

        return decorator

    def add_post(self, entry_type):
        """
        Add an unconditional post event handler
        """

        def decorator(func):
            self._post_webhook_handlers[entry_type] = func
            # if isinstance(text, (list, tuple)):
            #     for it in text:
            #         self.__add_handler(func, entry, text=it)
            # else:
            #     self.__add_handler(func, entry, text=text)

            return func

        return decorator

    def add_postback_handler(
        self, regexes: List[str] = None, quick_reply=True, button=True
    ):
        def wrapper(func):
            if regexes is None:
                return func

            for payload in regexes:
                if quick_reply:
                    self._quick_reply_callbacks[payload] = func
                if button:
                    self._button_callbacks[payload] = func

            return func

        return wrapper

    def set_uncaught_postback_handler(self, func):
        self.uncaught_postback_handler = func
        return func

    def get_quick_reply_callbacks(self, entry: MessagesEvent):
        callbacks = []
        for key in self._quick_reply_callbacks.keys():
            if key not in self._quick_reply_callbacks_key_regex:
                self._quick_reply_callbacks_key_regex[key] = re.compile(
                    key + "$"
                )

            if self._quick_reply_callbacks_key_regex[key].match(entry.payload):
                callbacks.append(self._quick_reply_callbacks[key])

        return callbacks

    def get_postback_callbacks(self, entry: PostbackEvent):
        callbacks = []
        for key in self._button_callbacks.keys():
            if key not in self._button_callbacks_key_regex:
                self._button_callbacks_key_regex[key] = re.compile(key + "$")

            if self._button_callbacks_key_regex[key].match(entry.payload):
                callbacks.append(self._button_callbacks[key])

        return callbacks
