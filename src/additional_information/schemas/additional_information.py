from pydantic import BaseModel

class AdditionalInformationSchema(BaseModel):
    comment: str

    class Config:
        orm_mode = True

class AdditionalInformationBaseModel(BaseModel):
    identifier: str
    gender: str
    age: int

    comment: str