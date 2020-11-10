from pydantic import BaseModel
from songmam.models.webhook.events.base import BaseMessaging, WithTimestamp


class GamePlay(BaseModel):
    game_id: str
    player_id: str
    context_type: str
    context_id: str
    score: int
    payload: str


class GamePlayEntries(BaseMessaging, WithTimestamp):
    game_play: GamePlay


# {
#   "recipient": {
#     "id": "<PSID>"
#   },
#   "recipient": {
#     "id": "<PAGE_ID>"
#   },
#   "timestamp": 1469111400000,
#   "game_play": {
#     "game_id": "<GAME-APP-ID>",
#     "player_id": "<PLAYER-ID>",
#     "context_type": "<CONTEXT-TYPE:SOLO|THREAD>",
#     "context_id": "<CONTEXT-ID>", # If a Messenger Thread context
#     "score": <SCORE-NUM>, # If a classic score based game
#     "payload": "<PAYLOAD>" # If a rich game
#   }
# }
