import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from fastapi import FastAPI 

from models import database, metadata, engine
from routes import web_app

app = FastAPI()
metadata.create_all(engine)


@app.on_event("startup")
async def startup() -> None:
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if database.is_connected:
        await database.disconnect()


app.include_router(web_app.route)
