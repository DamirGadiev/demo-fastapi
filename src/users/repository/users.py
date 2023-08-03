from sqlalchemy.orm import Session

from users.models.profiles import ProfileModel
from utils.database import engine


def create(data: dict, db: Session) -> ProfileModel:
    profile_obj = (
        db.query(ProfileModel)
        .filter(ProfileModel.identifier == data.get("identifier"))
        .first()
    )
    if not profile_obj:
        new_profile = ProfileModel(
            identifier=data.get("identifier"),
            gender=data.get("gender"),
            age=data.get("age"),
        )
        new_profile.save(db)
        return new_profile
    return profile_obj


def aggregate_by_profile():
    stmt = """
    select pr.identifier,
       pr.gender,
       pr.age,
       e.pattern_id,
       e.status,
       e.storage_name,
       e_v.created_at,
       e_v.valence,
       e_v.arousal,
       e_v.intensity,
       e_v.sharpness,
       e_v.roughness,
       e_v.regularity,
       e_v.shape_recognition,
       e_v.question_1,
       e_v.question_2,
       e_v.correct_hand_position_percentage
    from evaluation_experiment as e_v
         left join experiments e on e.id = e_v.experiment_id
         left outer join profiles pr on pr.id = e_v.profile_id order by pr.identifier;
    """
    with engine.connect() as conn:
        return [row for row in conn.execute(stmt)]
    return []
