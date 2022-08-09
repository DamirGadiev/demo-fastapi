import sqlalchemy

from models import metadata, database

evaluation_experiment = sqlalchemy.Table(
    "evaluation_experiment",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column("sensitivity_assessment", sqlalchemy.Integer, default=1),
    sqlalchemy.Column("mood_assessment", sqlalchemy.Integer, default=1),
    sqlalchemy.Column("description", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("profile_id", sqlalchemy.ForeignKey('profiles.id')),
    sqlalchemy.Column("experiment_id", sqlalchemy.ForeignKey('experiments.id')),
)


async def create_evaluation_experiment(sensitivity_assessment: int, mood_assessment: int, description: str,
                                       profile_id: int, experiment_id: int) -> int:
    query = evaluation_experiment.insert().values(
        sensitivity_assessment=sensitivity_assessment,
        mood_assessment=mood_assessment,
        description=description,
        profile_id=profile_id,
        experiment_id=experiment_id,
    )
    evaluation_experiment_id = await database.execute(query)
    return evaluation_experiment_id
