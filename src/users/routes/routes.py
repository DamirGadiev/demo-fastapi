import io
import os
import sys
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

from fastapi import APIRouter, Form
from fastapi import status, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from pandas import DataFrame

from users.repository.users import aggregate_by_profile

route = APIRouter(
    prefix="/profiles",
    tags=["profile"],
)

dir_p = os.path.abspath(os.path.join(dir_path, os.pardir)) + '/templates'
templates = Jinja2Templates(directory=dir_p)

@route.get("/summary", response_class=HTMLResponse)
def get_summary_page(request: Request):
    return HTMLResponse(summary_page)
    # return templates.TemplateResponse("summary_page.html", {"request": request})


@route.post("/summary", status_code=status.HTTP_200_OK)
def get_summary_data(password: str = Form("default_password")):
    if not password == "hybrid-ai-net":
        return templates.TemplateResponse(
            "summary_page.html", {"request": {"message": "Invalid personal password"}}
        )
    summary = aggregate_by_profile()
    result = [
        {
            "identifier": item.identifier,
            "gender": item.gender,
            "age": item.age,
            "pattern_id": item.pattern_id,
            "storage_name": item.storage_name,
            "status": item.status,
            "valence": item.valence,
            "arousal": item.arousal,
            "intensity": item.intensity,
            "sharpness": item.sharpness,
            "roughness": item.roughness,
            "regularity": item.regularity,
            "shape_recognition": item.shape_recognition,
            "question_1": item.question_1,
            "question_2": item.question_2,
            "correct_hand_position_percentage": item.correct_hand_position_percentage,
            "created_at": item.created_at,
        }
        for item in summary
    ]

    df = DataFrame(result)

    stream = io.StringIO()

    df.to_csv(stream, index=False)

    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")

    response.headers["Content-Disposition"] = "attachment; filename=export.csv"

    return response
