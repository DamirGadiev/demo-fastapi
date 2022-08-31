import io
from typing import List

from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import HTMLResponse, StreamingResponse
from pandas import DataFrame

from handlers.base_handler import MessageHandler
from managers.connection_managers import manager
from models.profiles import aggregate_by_profile
from schemas.web_app_shemas import SummaryDataModel

route = APIRouter()

template = """
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
<button onclick="newSession()">New session</button>
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

    function startExperiment() {
        ws.send(JSON.stringify({
            "type": "WEB_APP",
            "action": "WEB_APP_EXPERIMENT_START",
            "data": {},
            "status": {"type": "success", "description": "Experiment initiated from webapp"},
            "message": "Start the experiment"
        }))
    }

    function repeatExperiment() {
        ws.send(JSON.stringify({
            "type": "WEB_APP",
            "action": "WEB_APP_EXPERIMENT_START",
            "data": {"pattern_id": "circle.csv"},
            "status": {"type": "success", "description": "Experiment repeat from webapp"},
            "message": "Repeat the experiment"
        }))
    }

    function stopExperiment() {
        ws.send(JSON.stringify({
            "type": "WEB_APP",
            "action": "WEB_APP_EXPERIMENT_STOP",
            "data": {},
            "status": {"type": "success", "description": "Experiment stopped from webapp"},
            "message": "Stop the experiment"
        }))
    }

    function finishExperiment() {
        ws.send(JSON.stringify({
            "type": "EXPERIMENT",
            "action": "EXPERIMENT_FINISHED",
            "data": {
                "reason": "no errors occured",
                "pattern_id": "cicrle.csv"
            },
            "status": {"type": "success", "description": "Experiment finished from webapp"},
            "message": "Current experiment is finished."
        }))
    }

    function newSession() {
        ws.send(JSON.stringify({
            "type": "WEB_APP",
            "action": "WEB_APP_NEW_SESSION",
            "data": {},
            "status": {"type": "success", "description": "Experiment new session in webapp"},
            "message": "New session initiated from webapp"
        }))
    }

    function deviceConnectionReady() {
        ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_CONNECTION_OPEN",
            "data": {},
            "status": {"type": "success", "description": "Device initiated from webapp"},
            "message": "Connection is open."
        }))
    }

    function deviceUltraleapReady() {
        ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_ULTRALEAP_READY",
            "data": {},
            "status": {"type": "success", "description": "Device Ultraleap ready"},
            "message": "Ultraleap device is ready."
        }))
    }

    function deviceCameraReady() {
        ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_CAMERA_READY",
            "data": {},
            "status": {"type": "success", "description": "Device Camera ready"},
            "message": "Camera connection established."
        }))
    }

    function devicePatternsReady() {
        ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_PATTERNS_READY",
            "data": {},
            "status": {"type": "success", "description": "Device Patterns ready"},
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
            "status": {"type": "success", "description": "Device Active Patterns ready"},
            "message": "Active pattern is ready."
        }))
    }
</script>
</body>

</html>

"""


@route.get("/")
async def get():
    return HTMLResponse(template)


@route.websocket("/device/{client_id}/{device_type}")
async def websocket_endpoint(websocket: WebSocket, client_id, device_type):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await MessageHandler.process_message(websocket, data, manager)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(websocket, str({"type": "DEVICE", "action": "DISCONNECT", "data": {},
                                                "status": {"type": "success",
                                                           "description": f"{device_type} disconnected"},
                                                "message": f"#{device_type} left the chat #{client_id}"}))


@route.get("/summary", response_model=List[SummaryDataModel])
async def get_summary():
    summary = await aggregate_by_profile()
    result = [
        {
            "id": item.id,
            "identifier": item.identifier,
            "gender": item.gender,
            "age": item.age, "mood_assessment": item.mood_assessment,
            "sensitivity_assessment": item.sensitivity_assessment,
            "correct_hand_position_procentage": f"{item.correct_hand_position_procentage:.10f}",
            "description": item.description,
            "pattern_id": item.pattern_id,
            "status": item.status
        }
        for item in summary
    ]

    df = DataFrame(result)

    stream = io.StringIO()

    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]),
                                 media_type="text/csv"
                                 )

    response.headers["Content-Disposition"] = "attachment; filename=export.csv"

    return response
