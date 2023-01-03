from pydantic import BaseModel


class ProfileBaseSchema(BaseModel):
    identifier: str
    gender: str
    age: int


class ProfileSchema(ProfileBaseSchema):
    identifier: str
    gender: str
    age: int

    class Config:
        orm_mode = True


class AdministratorSchema(BaseModel):
    username: str
    password: str
