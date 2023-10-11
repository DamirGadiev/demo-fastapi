from pydantic import BaseModel


class ExperimentDataModel(BaseModel):
    identifier: str
    gender: str
    hand: str
    age: int

    pattern_id: str
    pattern_name: str
    storage_name: str

    valence: int
    arousal: int
    intensity: float
    sharpness: int
    roughness: int
    regularity: int
    shape_recognition: int
    correct_hand_position_percentage: float
    question_1: str
    question_2: str


class ExperimentDataSchema(BaseModel):
    valence: int
    arousal: int
    intensity: float
    sharpness: int
    roughness: int
    regularity: int
    shape_recognition: int
    correct_hand_position_percentage: float
    question_1: str
    question_2: str

    class Config:
        orm_mode = True
