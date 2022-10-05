import sqlalchemy

from models import metadata, database

evaluation_experiment = sqlalchemy.Table(
    "evaluation_experiment",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column("valence", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("arousal", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("intensity", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("sharpness", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("roughness", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("regularity", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("shape_recognition", sqlalchemy.Integer, default=0),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("question_1", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("question_2", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("correct_hand_position_procentage", sqlalchemy.DECIMAL),
    sqlalchemy.Column("profile_id", sqlalchemy.ForeignKey('profiles.id')),
    sqlalchemy.Column("experiment_id", sqlalchemy.ForeignKey('experiments.id')),
)


async def create_evaluation_experiment(
        valence: int, arousal: int, intensity: int,
        sharpness: int, roughness: int, regularity: int,
        shape_recognition, description: str, question_1: str,
        question_2: str, correct_hand_position_procentage: int,
        profile_id: int, experiment_id: int
) -> int:
    query = evaluation_experiment.insert().values(
        valence=valence,
        arousal=arousal,
        intensity=intensity,
        sharpness=sharpness,
        roughness=roughness,
        regularity=regularity,
        shape_recognition=shape_recognition,
        description=description,
        question_1=question_1,
        question_2=question_2,
        correct_hand_position_procentage=correct_hand_position_procentage,
        profile_id=profile_id,
        experiment_id=experiment_id,
    )
    evaluation_experiment_id = await database.execute(query)
    return evaluation_experiment_id
