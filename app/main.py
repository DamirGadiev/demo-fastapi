from typing import List, Dict

import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import logging
from handlers.base_handler import MessageHandler
from models import database #, metadata, engine

app = FastAPI()

#metadata.create_all(engine)

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
    <button onclick="repeatExperiment()">Repeat experiment</button>
    <button onclick="stopExperiment()">Stop experiment</button>
    <button onclick="finishExperiment()">Finish experiment</button>
    <button onclick="deviceConnectionReady()">Device connection ready</button>
    <button onclick="deviceUltraleapReady()">Device ultraleap ready</button>
    <button onclick="devicePatternsReady()">Device patterns ready</button>
    <button onclick="deviceCameraReady()">Device camera ready</button>
    <button onclick="deviceActivePatternReady()">Device Active Pattern Ready</button>
    <ul id="messages">
    </ul>
    <script>
        var client_id = "client_id_test"
        document.querySelector("#ws-id").textContent = client_id;
        var ws = new WebSocket(`ws://touchlesssurveyapp.azurewebsites.net/device/${client_id}/WEB_APP`);
        ws.onmessage = function (event) {
            var messages = document.getElementById("messages")
            var message = document.createElement("li")
            var content = document.createTextNode(event.data)
            message.appendChild(content)
            messages.appendChild(message)
        };
        ws.onerror = function (event) {
            console.log("Error happened!");
            console.log(event);
        }
        function startExperiment() {
            ws.send(JSON.stringify({ "type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_START", "data": {}, "message": "Start the experiment" }))
        }
        function repeatExperiment() {
            ws.send(JSON.stringify({ "type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_START", "data": {"pattern_id": "circle.csv"}, "message": "Repeat the experiment" }))
        }
        function stopExperiment() {
            ws.send(JSON.stringify({ "type": "WEB_APP", "action": "WEB_APP_EXPERIMENT_STOP", "data": {}, "message": "Stop the experiment" }))
        }
        function finishExperiment() {
            ws.send(JSON.stringify({
                "type": "EXPERIMENT",
                "action": "EXPERIMENT_FINISHED",
                "data": {
                    "reason": "no errors occured",
                    "pattern_id": "cicrle.csv"
                },
                "message": "Current experiment is finished."
            }))
        }
        function deviceConnectionReady() {
            ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_CONNECTION_OPEN",
            "data": {},
            "message": "Connection is open."
            }))
        }
        function deviceUltraleapReady() {
            ws.send(JSON.stringify({
                "type": "DEVICE",
                "action": "DEVICE_ULTRALEAP_READY",
                "data": {},
                "message": "Ultraleap device is ready."
            }))
        }
        function deviceCameraReady() {
            ws.send(JSON.stringify({
                "type": "DEVICE",
                "action": "DEVICE_CAMERA_READY",
                "data": {},
                "message": "Camera connection established."
            }))
        }
        function devicePatternsReady() {
            ws.send(JSON.stringify({
                "type": "DEVICE",
                "action": "DEVICE_PATTERNS_READY",
                "data": {},
                "message": "Patterns are ready."
            }))
        }
        function deviceActivePatternReady() {
            ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_ACTIVE_PATTERN_READY",
            "data": {
                "pattern_id": "circle.csv"
            },
            "message": "Active pattern is ready."
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
