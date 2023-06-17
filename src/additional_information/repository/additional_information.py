from sqlalchemy.orm import Session

from additional_information.models.additional_information import AdditionalInformationModel


def create(data: dict, db: Session) -> AdditionalInformationModel:
    experiment_obj = (
        db.query(AdditionalInformationModel)
        .filter(AdditionalInformationModel.profile_id == data.get("profile_id"))
        .first()
    )
    if not experiment_obj:
        experiment_obj = AdditionalInformationModel(
            comment=data.get("comment"),
            profile_id=data.get("profile_id"),
        )
        experiment_obj.save(db)
    return experiment_obj
