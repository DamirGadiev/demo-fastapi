from typing import List
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
print("here we are=========")
print(os.path.abspath(os.path.join(dir_path, os.pardir)))
print("and there we are")
# exit()

print(os.path.abspath)


from fastapi import WebSocket, WebSocketDisconnect, Request, APIRouter
from fastapi.templating import Jinja2Templates

from handlers.base_handler import MessageHandler
from managers.connection_managers import manager
from models.profiles import aggregate_by_profile
from schemas.web_app_shemas import SummaryDataModel

route = APIRouter()

dir_p = os.path.abspath(os.path.join(dir_path, os.pardir)) + '/templates'
templates = Jinja2Templates(directory=dir_p)


@route.get("/")
async def get(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


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
                                                "message": f"#{device_type} left the chat #{client_id}"}))


@route.get("/summary", response_model=List[SummaryDataModel])
async def get_summary():
    summary = await aggregate_by_profile()
    return summary
