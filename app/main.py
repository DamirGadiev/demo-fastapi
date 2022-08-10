from typing import List, Dict
import sys
import os

print("-========================-")
print(sys.path)
dir_path = os.path.dirname(os.path.realpath(__file__)) + '/app'
print(dir_path)
sys.path.append(dir_path)
print(sys.path)
print("-=====================-")
# sys.path.append( '/handlers' )
# sys.path.append('/models')

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import logging
from handlers.base_handler import MessageHandler
from models import database  # , metadata, engine

app = FastAPI()

# metadata.create_all(engine)

html = """
<!DOCTYPE html>
<html>

<head>
    <title>Connected device</title>
</head>

<body>
    <h1>Events channel</h1>
    <h2>Your ID: <span id="ws-id"></span></h2>
    <button onclick="startExperiment()">Start experiment</button>
    <button onclick="stopExperiment()">Stop experiment</button>
    <button onclick="finishExperiment()">Finish experiment</button>
    <ul id="messages">
    </ul>
    <script>
        var client_id = "client_id_test"
        document.querySelector("#ws-id").textContent = client_id;
        var ws = new WebSocket(`ws://localhost:9991/device/${client_id}/WEB_APP`);
        ws.onmessage = function (event) {
            var messages = document.getElementById("messages")
            var message = document.createElement("li")
            var content = document.createTextNode(event.data)
            message.appendChild(content)
            messages.appendChild(message)
        };
        function startExperiment() {
            ws.send(JSON.stringify({ "type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_START", "data": {}, "message": "" }))
        }
        function stopExperiment() {
            ws.send(JSON.stringify({ "type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_STOP", "data": {}, "message": "" }))
        }
        function finishExperiment() {
            ws.send(JSON.stringify({
                "type": "EXPERIMENT",
                "action": "EXPERIMENT_FINISHED",
                "data": {
                    "reason": "no errors occured",
                    "pattern_id": 12345
                },
                "message": "Current experiment is finished."
            }))
        }
    </script>
</body>

</html>
"""


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

        await manager.broadcast(websocket, str({"type": "DEVICE", "action": "CONNECT", "data": {},
                                                "message": f"#{device_type} joined the channel"}))

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

    async def broadcast(self, websocket, message: str):
        client_id = websocket.path_params["client_id"]
        device_type = websocket.path_params["device_type"]
        for key in self.active_connections.get(client_id, {}):
            if key is not device_type:
                for connection in self.active_connections.get(client_id, {}).get(key):
                    await connection.send_text(message)


manager = ConnectionManager()


@app.on_event("startup")
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if database.is_connected:
        await database.disconnect()


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/device/{client_id}/{device_type}")
async def websocket_endpoint(websocket: WebSocket, client_id, device_type):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await MessageHandler.process_message(websocket, data, manager)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(websocket, str({"type": "DEVICE", "action": "DISCONNECT", "data": {},
                                                "message": f"#{device_type} left the chat #{client_id}"}))
