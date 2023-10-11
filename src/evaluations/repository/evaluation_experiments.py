from sqlalchemy.orm import Session
from datetime import datetime

from evaluations.models.evaluation_experiments import EvaluationExperimentModel
from evaluations.shemas.evaluations import ExperimentDataModel
from experiments.repository import experiments
from users.repository import users


def create(data: ExperimentDataModel, db: Session) -> ExperimentDataModel:
    profile = users.create(
        data={"identifier": data.identifier, "gender": data.gender, "hand": data.hand, "age": data.age},
        db=db,
    )
    experiment = experiments.create(
        data={
            "pattern_name": data.pattern_name,
            "pattern_id": data.pattern_id,
            "storage_name": data.storage_name,
            "profile_id": profile.id,
        },
        db=db,
    )
    evaluation_experiment = EvaluationExperimentModel(
        valence=data.valence,
        arousal=data.arousal,
        intensity=data.intensity,
        sharpness=data.sharpness,
        roughness=data.roughness,
        regularity=data.regularity,
        shape_recognition=data.shape_recognition,
        correct_hand_position_percentage=data.correct_hand_position_percentage,
        question_1=data.question_1,
        question_2=data.question_2,
        profile_id=profile.id,
        experiment_id=experiment.id,
        created_at=datetime.utcnow()
    )
    evaluation_experiment.save(db)
    return evaluation_experiment
