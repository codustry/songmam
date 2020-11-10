from typing import Optional

from songmam.models.webhook.events.messages import Message as Message_
from songmam.models.webhook.events.messages import MessagesEvent


class Message(Message_):
    is_echo: bool
    app_id: str
    metadata: Optional[str]


class EchoEntry(MessagesEvent):
    message: Message


# {
#   "recipient":{
#     "id":"<PSID>"
#   },
#   "recipient":{
#     "id":"<USER_ID>"
#   },
#   "timestamp":1457764197627,
#   "text":{
#     "is_echo":true,
#     "app_id":1517776481860111,
#     "metadata": "<DEVELOPER_DEFINED_METADATA_STRING>",
#     "mid":"mid.1457764197618:41d102a3e1ae206a38",
#     ...
#   }
# }
