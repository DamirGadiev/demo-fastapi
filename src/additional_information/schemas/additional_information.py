from pydantic import BaseModel

class AdditionalInformationBaseSchema(BaseModel):
    comment: str

class AdditionalInformationSchema(AdditionalInformationBaseSchema):
    identifier: str
    gender: str
    age: int

    class Config:
        orm_mode = True