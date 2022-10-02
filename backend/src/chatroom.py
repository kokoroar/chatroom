import json
import logging.config
from logging import getLogger
from pathlib import Path
from typing import Final

import yaml
from websocket_server import WebsocketServer

ROOT: Final[Path] = Path(__file__).resolve().parent
with open(ROOT / "logging.conf.yaml", mode="r") as f:
    logging.config.dictConfig(yaml.safe_load(f.read()))

logger: Final = getLogger(__name__)


class ChatPost(object):
    def __init__(self, from_, message) -> None:
        self.from_ = from_
        self.message = message

    def to_json(self):
        return json.dumps({"from": self.from_, "message": self.message})


class ChatRoom(object):
    server: WebsocketServer

    def __init__(self, port: int, host: str):
        self.messages = []
        self.server = WebsocketServer(host=host, port=port, loglevel=logging.INFO)
        self.server.set_fn_new_client(self._new_client)
        self.server.set_fn_message_received(self._message_received)

    def _new_client(self, client, server) -> None:
        logger.info(f"New user connected {client['id']}")
        self._post_message(ChatPost("system", f"New user connected {client['id']}"))

    def _message_received(self, client, server, message):
        logger.info(f"From {client['id']}: {message}")
        self._post_message(ChatPost(client["id"], message))

    def _post_message(self, message: ChatPost):
        self.server.send_message_to_all(message.to_json())

    def run(self):
        self.server.run_forever()


if __name__ == "__main__":
    room = ChatRoom(80, "0.0.0.0")
    room.run()
