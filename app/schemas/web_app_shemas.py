from pydantic import BaseModel

from models.experiments import ExperimentStatusEnum
from models.profiles import GenderEnum


class MessageModel(BaseModel):
    type: str
    action: str
    data: dict = {}
    message: str


class ProfileModel(BaseModel):
    gender: str
    age: int


class ExperimentStatusModel(BaseModel):
    profile_id: int
    experiment_id: int


class ExperimentModel(BaseModel):
    pattern_id: str
    pattern_name: str = None
    profile_id: str


class EvaluationExperimentModel(BaseModel):
    sensitivity_assessment: int
    mood_assessment: int
    description: str = ''
    profile_id: int = None
    experiment_id: int = None


class ExperimentDataModel(BaseModel):
    pattern_id: str
    pattern_name: str = ''
    gender: str
    age: int
    identifier: str
    sensitivity_assessment: int
    mood_assessment: int
    description: str = ''


class SummaryDataModel(BaseModel):
    id: int
    identifier: str
    gender: GenderEnum
    age: int
    mood_assessment: int
    sensitivity_assessment: int
    description: str
    pattern_id: str
    status: ExperimentStatusEnum

    class Config:
        orm_mode = True
        use_enum_values = True
