from pydantic import BaseModel

from models.experiments import ExperimentStatusEnum
from models.profiles import GenderEnum


class MessageModel(BaseModel):
    type: str
    action: str
    data: dict
    status: dict
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
    # description: str = ''
    profile_id: int = None
    experiment_id: int = None


class ExperimentDataModel(BaseModel):
    pattern_id: str
    pattern_name: str = ''
    gender: str
    age: int
    valence: int
    arousal: int
    intensity: int
    sharpness: int
    roughness: int
    regularity: int
    shape_recognition: int
    # description: int
    question_1: str
    question_2: str
    correct_hand_position_procentage: int
    identifier: str
    correct_hand_position_procentage: float


class SummaryDataModel(BaseModel):
    id: int
    identifier: str
    gender: GenderEnum
    age: int
    valence: int
    arousal: int
    intensity: int
    sharpness: int
    roughness: int
    regularity: int
    shape_recognition: int
    question_1: str
    question_2: str
    correct_hand_position_procentage: int
    # description: str
    pattern_id: str
    status: ExperimentStatusEnum

    class Config:
        orm_mode = True
        use_enum_values = True
