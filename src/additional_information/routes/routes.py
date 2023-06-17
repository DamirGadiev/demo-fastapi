from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from additional_information.repository import additional_information
from additional_information.schemas.additional_information import AdditionalInformationBaseSchema, AdditionalInformationSchema
from utils.database import get_db

route = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


@route.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=AdditionalInformationBaseSchema
)
def create(request: AdditionalInformationSchema, db: Session = Depends(get_db)):
    return additional_information.create(request, db)
