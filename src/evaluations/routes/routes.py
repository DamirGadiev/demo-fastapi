from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from evaluations.repository import evaluation_experiments
from evaluations.shemas.evaluations import ExperimentDataModel, ExperimentDataSchema
from utils.database import get_db

route = APIRouter(
    prefix="/evaluations",
    tags=["evaluations"],
)


@route.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=ExperimentDataSchema
)
def create(request: ExperimentDataModel, db: Session = Depends(get_db)):
    return evaluation_experiments.create(request, db)
