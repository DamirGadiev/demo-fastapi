from enum import Enum

import sqlalchemy

from models import metadata, database


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
    query = profile.insert().values(
        gender=gender,
        identifier=identifier,
        age=age
    )
    profile_id = await database.execute(query)
    return profile_id
