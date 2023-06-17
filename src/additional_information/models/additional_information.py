from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Session

from utils.database import Base

class AdditionalInformationModel(Base):
    __tablename__ = "additional_information"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=True, default="")
    created_at = Column(DateTime, default=datetime.utcnow())
    profile_id = Column(Integer, ForeignKey("profiles.id"))

    def __repr__(self):
        return f"<Experiments: {self.id}|{self.comment}>"

    def __str__(self):
        return f"Experiments: {self.id}|{self.comment}"

    def save(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    def update(self, db: Session):
        db.commit()

    def delete(self, db: Session):
        db.delete(self)
        db.commit()
