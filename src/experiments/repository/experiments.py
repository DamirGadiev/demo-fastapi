from sqlalchemy.orm import Session
from datetime import datetime

from experiments.models.experiments import ExperimentModel


def create(data: dict, db: Session) -> ExperimentModel:
    experiment_obj = (
        db.query(ExperimentModel)
        .filter(ExperimentModel.pattern_id == data.get("pattern_id"))
        .first()
    )
    if not experiment_obj:
        experiment_obj = ExperimentModel(
            pattern_name=data.get("pattern_name"),
            pattern_id=data.get("pattern_id"),
            storage_name=data.get("storage_name"),
            profile_id=data.get("profile_id"),
            created_at=datetime.utcnow()
        )
        experiment_obj.save(db)
    return experiment_obj
