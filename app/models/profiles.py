from enum import Enum

import sqlalchemy
from sqlalchemy import select

from models import metadata, database, engine
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
    stmt = """
    select pr.identifier,
       pr.gender,
       pr.age,
       e.pattern_id,
       e.status,
       e_v.valence,
       e_v.arousal,
       e_v.intensity,
       e_v.sharpness,
       e_v.roughness,
       e_v.regularity,
       e_v.shape_recognition,
       e_v.question_1,
       e_v.question_2,
       e_v.correct_hand_position_procentage
from evaluation_experiment as e_v
         left join experiments e on e.id = e_v.experiment_id
         left outer join profiles pr on pr.id = e_v.profile_id;
    """
    with engine.connect() as conn:
        return [row for row in conn.execute(stmt)]
    return []
