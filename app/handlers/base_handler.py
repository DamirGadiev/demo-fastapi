import json

from fastapi import WebSocket

from handlers.device_handler import DeviceMessageHandler
from handlers.experiment_handler import ExperimentMessageHandler
from handlers.web_app_handler import WebAppMessageHandler
from schemas.web_app_shemas import MessageModel


class MessageHandler:

    @classmethod
    async def process_message(cls, websocket: WebSocket, data: str, manager):
        data = json.loads(data)
        message = MessageModel(**data)
        if message.type == "WEB_APP":
            await WebAppMessageHandler.process(websocket, message, manager)
        elif message.type == "DEVICE":
            await DeviceMessageHandler.process(websocket, message, manager)
        elif message.type == "EXPERIMENT":
            await ExperimentMessageHandler.process(websocket, message, manager)
        else:
            await manager.broadcast(websocket, str({
                "type": "WEB_APP",
                "action": "",
                "data": {},
                "status": {"type": "error", "description": "Unknown connection"},
                "message": "Unknown connection"
            }))
