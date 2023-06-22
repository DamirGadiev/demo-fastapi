from sqlalchemy.orm import Session

from additional_information.models.additional_information import AdditionalInformationModel
from additional_information.schemas.additional_information import AdditionalInformationSchema, AdditionalInformationBaseModel
from users.repository import users

def create(data: AdditionalInformationBaseModel, db: Session) -> AdditionalInformationBaseModel:
    profile = users.create(
        data = {"identifier": data.identifier, "gender": data.gender, "age": data.age},
        db=db
    )
    additional_information = AdditionalInformationModel(
        comment=data.comment,
        profile_id = profile.id
    )
    additional_information.save(db)
    return additional_information