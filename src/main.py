import models
from config import Config
from utils.database import engine

if Config.IS_AZURE_ENVIRONMENT:
    import os
    import sys

    dir_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(dir_path)

from fastapi import FastAPI

from users.routes.routes import route as user_route
from evaluations.routes.routes import route as evaluation_route

app = FastAPI(debug=True)
models.Base.metadata.create_all(engine)

app.include_router(user_route)
app.include_router(evaluation_route)
