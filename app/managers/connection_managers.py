import logging
from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict = {}
        self.log = logging.getLogger(name="LoggerBy")

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        client_id = websocket.path_params["client_id"]
        device_type = websocket.path_params["device_type"]

        if not self.active_connections.get(client_id):
            self.active_connections[client_id] = {}

        if not self.active_connections.get(client_id).get(device_type):
            self.active_connections.get(client_id)[device_type] = []

        self.active_connections.get(client_id).get(device_type).append(websocket)

        await manager.broadcast(websocket, str({
            "type": "DEVICE",
            "action": "CONNECT",
            "data": {},
            "status": {"type": "success", "description": f"{device_type} connected"},
            "message": f"#{device_type} joined the channel"
        }))

    def disconnect(self, websocket: WebSocket):
        client_id = websocket.path_params["client_id"]
        device_type = websocket.path_params["device_type"]
        if self.active_connections.get(client_id):
            if self.active_connections.get(client_id).get(device_type):
                self.active_connections.get(client_id).get(device_type).remove(websocket)
                if not self.active_connections.get(client_id).get(device_type):
                    self.active_connections.get(client_id).pop(device_type)
            if not self.active_connections.get(client_id):
                self.active_connections.pop(client_id)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, websocket: WebSocket, message: str):
        client_id = websocket.path_params["client_id"]
        device_type = websocket.path_params["device_type"]
        for key in self.active_connections.get(client_id, {}):
            if key is not device_type:
                for connection in self.active_connections.get(client_id, {}).get(key):
                    try:
                        await connection.send_text(message)
                    except BaseException as e:
                        pass


manager = ConnectionManager()
