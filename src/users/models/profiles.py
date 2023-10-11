from enum import Enum

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import Session

from utils.database import Base


class GenderEnum(Enum):
    male = "male"
    female = "female"
    other = "other"

class HandEnum(Enum):
    right = "right"
    left = "left"

class ProfileModel(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String, default="")
    gender = Column(String, default=GenderEnum.other)
    hand = Column(String, default=HandEnum.right)
    age = Column(Integer, default=0)

    def __repr__(self):
        return f"<Profile: {self.id}|{self.gender}|{self.hand}|{self.age}>"

    def __str__(self):
        return f"Profile: {self.id}|{self.gender}|{self.hand}|{self.age}"

    def save(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    def update(self, db: Session):
        db.commit()

    def delete(self, db: Session):
        db.delete(self)
        db.commit()
