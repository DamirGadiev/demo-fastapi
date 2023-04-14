from datetime import datetime

from sqlalchemy import Column, Integer, DECIMAL, ForeignKey, DateTime, String
from sqlalchemy.orm import Session

from utils.database import Base


class EvaluationExperimentModel(Base):
    __tablename__ = "evaluation_experiment"

    id = Column(Integer, primary_key=True, index=True)
    valence = Column(Integer, nullable=True, default=0)
    arousal = Column(Integer, nullable=True, default=0)
    intensity = Column(DECIMAL, nullable=True, default=0.0)
    sharpness = Column(Integer, nullable=True, default=0)
    roughness = Column(Integer, nullable=True, default=0)
    regularity = Column(Integer, nullable=True, default=0)
    shape_recognition = Column(Integer, nullable=True, default=0)
    correct_hand_position_percentage = Column(DECIMAL, nullable=True, default=0.0)
    question_1 = Column(String, nullable=True, default=0)
    question_2 = Column(String, nullable=True, default=0)
    created_at = Column(DateTime, default=datetime.utcnow())

    profile_id = Column(Integer, ForeignKey("profiles.id"))
    experiment_id = Column(Integer, ForeignKey("experiments.id"))

    def __repr__(self):
        return f"<EvaluationExperiment: {self.id}>"

    def __str__(self):
        return f"EvaluationExperiment: {self.id}"

    def save(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    def update(self, db: Session):
        db.commit()

    def delete(self, db: Session):
        db.delete(self)
        db.commit()
