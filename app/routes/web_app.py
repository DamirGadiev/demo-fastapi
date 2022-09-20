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
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
</head>

<body>
<div class="container">
    <h1>Events channel</h1>
    <div class="alert alert-secondary" role="alert" style="width: 18rem;">
      <b>Your ID:</b> <span id="ws-id"></span>
    </div>
    <div class="container" style="display: flex; flex-wrap: wrap;">
        <div class="card" style="width: 18rem; margin-right: 20px;">
            <div class="card-header">
                Experiment Workflow
            </div>
            <ul class="list-group">
                <li class="list-group-item"><button type="button" class="btn btn-success" onclick="startExperiment()">Start experiment</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-success" onclick="newSession()">New session</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-success" onclick="repeatExperiment()">Repeat experiment</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-success" onclick="finishExperiment()">Finish experiment</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-danger" onclick="stopExperiment()">Stop experiment</button></li>
            </ul>
        </div>
        <div class="card" style="width: 18rem; margin-right: 20px;">
            <div class="card-header">
                Devices Workflow
            </div>
            <ul class="list-group">
                <li class="list-group-item"><button type="button" class="btn btn-success" onclick="deviceConnectionReady()">Device connection ready</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-success" onclick="deviceUltraleapReady()">Device ultraleap ready</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-success" onclick="devicePatternsReady()">Device patterns ready</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-success" onclick="deviceCameraReady()">Device camera ready</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-success" onclick="deviceActivePatternReady()">Device Active Pattern Ready</button></li>
            </ul>
        </div>
        <div class="card" style="width: 18rem; margin-right: 20px;">
            <div class="card-header">
                Testing Functionality
            </div>
            <ul class="list-group">
                <li class="list-group-item"><button type="button" class="btn btn-primary" onclick="evaluationForm()">Evaluation form</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-danger" onclick="cameraStopped()">Device camera stopped</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-danger" onclick="patternStopped()">Device pattern error</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-danger" onclick="activePatternStopped()">Device active pattern error</button></li>
                <li class="list-group-item"><button type="button" class="btn btn-danger" onclick="ultraleapStopped()">Device ultraleap stopped</button></li>
            </ul>
        </div>
    </div>
    <hr>
    <ul id="messages" class="list-group list-group-flush">
        <div class="card-header">
            <b><h3>EVENT LOG:</h3></b> 
        </div>
    </ul>
</div>
<script>
    var client_id = "client_id_test"
    document.querySelector("#ws-id").textContent = client_id;
    var ws = new WebSocket(`ws://touchlesssurveyapp.azurewebsites.net/device/${client_id}/WEB_APP`);
    ws.onmessage = function (event) {
        var messages = document.getElementById("messages")
        var message = document.createElement("li")
        message.classList.add('list-group-item');
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
    function cameraStopped() {
        ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_CAMERA_STOPPED",
            "data": {},
            "status": {"type": "error", "description": "Camera connection broken."},
            "message": "Camera connection broken."
        }))
    }
    function patternStopped() {
        ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_PATTERNS_ERROR",
            "data": {},
            "status": {"type": "error", "description": "An error occured while loading patterns from Azure cloud."},
            "message": "Loading patterns error."        
        }))
    }
    function activePatternStopped() {
        ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_ACTIVE_PATTERN_ERROR",
            "data": {},
            "status": {"type": "error", "description": "Error occured while using active pattern."},
            "message": "Active pattern error - does not exist."
        }))
    }
    function ultraleapStopped() {
        ws.send(JSON.stringify({
            "type": "DEVICE",
            "action": "DEVICE_ULTRALEAP_STOPPED",
            "data": {},
            "status": {"type": "error", "description": "Something went wrong with the ultraleap connection"},
            "message": "Ultraleap device has stopped."
        }))
    }
    function evaluationForm() {
        ws.send(JSON.stringify({
            "type": "WEB_APP",
            "action": "WEB_APP_EVALUATION_FORM",
            "data": {
                "pattern_id": "cicrle.csv",
                "correct_hand_position_procentage": 0,
                "age": 87,
                "gender": "female",
                "sensitivity_assessment": 6,
                "mood_assessment": 4,
                "description": "lorem",
                "identifier": "l;mkdjaiuhfinqerq",
            },
            "status": {"type": "success", "description": "Evaluation form and send to webapp"},
            "message": "Experiment evaluated from webapp"
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
            type: "WEB_APP",
            action: "WEB_APP_NEW_SESSION",
            data: {},
            status: {"type": "success", "description": "Experiment new session in webapp"},
            message: "New session initiated from webapp"
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
