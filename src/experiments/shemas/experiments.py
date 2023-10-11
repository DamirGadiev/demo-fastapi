from pydantic import BaseModel


class ExperimentBaseSchema(BaseModel):
    pattern_name: str
    pattern_id: str
    storage_name: str


class ExperimentSchema(ExperimentBaseSchema):
    identifier: str
    gender: str
    hand: str
    age: int

    class Config:
        orm_mode = True
