from datetime import datetime
from enum import Enum

import sqlalchemy
from sqlalchemy.sql import func

from models import metadata, database


class ExperimentStatusEnum(Enum):
    new = 'new'
    repeat = 'repeat'
    running = 'running'
    finished = 'finished'
    stopped = 'stopped'
    failed = 'failed'


experiment = sqlalchemy.Table(
    "experiments",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column("pattern_name", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("pattern_id", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.Enum(ExperimentStatusEnum), default=ExperimentStatusEnum.new),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, server_default=func.now()),
    sqlalchemy.Column("finished_at", sqlalchemy.DateTime, nullable=True),
    sqlalchemy.Column("profile_id", sqlalchemy.ForeignKey('profiles.id')),
)


async def create_experiment(pattern_name: str, pattern_id: str, profile_id: int) -> int:
    query = experiment.insert().values(
        pattern_name=pattern_name,
        pattern_id=pattern_id,
        status=ExperimentStatusEnum.new,
        profile_id=profile_id,
    )
    experiment_id = await database.execute(query)
    return experiment_id


async def update_experiment_status(_id: int, profile_id: int, status: ExperimentStatusEnum) -> int:
    query = experiment.update().where(
        experiment.c.id == _id,
        experiment.c.profile_id == profile_id
    ).values(
        status=status,
        finished_at=datetime.utcnow()
    )
    experiment_id = await database.execute(query)
    return experiment_id
