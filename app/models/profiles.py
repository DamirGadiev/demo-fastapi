from enum import Enum

import sqlalchemy
from sqlalchemy import select

from models import metadata, database
from models.evaluation_experiments import evaluation_experiment
from models.experiments import experiment


class GenderEnum(Enum):
    male = 'male'
    female = 'female'
    other = 'other'


profile = sqlalchemy.Table(
    "profiles",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, unique=True, autoincrement=True),
    sqlalchemy.Column("identifier", sqlalchemy.String(75)),
    sqlalchemy.Column("gender", sqlalchemy.Enum(GenderEnum)),
    sqlalchemy.Column("age", sqlalchemy.Integer),
)


async def create_profile(gender: str, age: int, identifier: str) -> int:
    query = profile.select().where(profile.c.identifier == identifier)
    profile_obj = await database.fetch_one(query)
    if not profile_obj:
        query = profile.insert().values(
            gender=gender,
            identifier=identifier,
            age=age
        )
        return await database.execute(query)
    return profile_obj.id


async def aggregate_by_profile():
    query = profile.join(
        evaluation_experiment, profile.c.id == evaluation_experiment.c.profile_id
    ).join(
        experiment, profile.c.id == experiment.c.profile_id
    )
    stmt = select(profile, evaluation_experiment, experiment).select_from(query)
    return await database.fetch_all(stmt)
