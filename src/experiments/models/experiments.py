from datetime import datetime

from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Session

from utils.database import Base


class ExperimentStatusEnum(Enum):
    new = "new"
    repeat = "repeat"
    running = "running"
    finished = "finished"
    stopped = "stopped"
    failed = "failed"


class ExperimentModel(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    pattern_name = Column(String, nullable=True, default="")
    pattern_id = Column(String, nullable=True, default="")
    storage_name = Column(String, nullable=True, default="")
    status = Column(String, default=ExperimentStatusEnum.new)
    created_at = Column(DateTime, default=datetime.utcnow())
    finished_at = Column(DateTime, nullable=True)

    profile_id = Column(Integer, ForeignKey("profiles.id"))

    def __repr__(self):
        return f"<Experiments: {self.id}|{self.pattern_name}|{self.status}>"

    def __str__(self):
        return f"Experiments: {self.id}|{self.pattern_name}|{self.status}"

    def save(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)

    def update(self, db: Session):
        db.commit()

    def delete(self, db: Session):
        db.delete(self)
        db.commit()
