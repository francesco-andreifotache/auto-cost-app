from sqlalchemy.orm import Session
from app.db_models.car_cost import CarCost

def get_history(db: Session, user_id: int, limit: int = 10):
    return (
        db.query(CarCost)
        .filter(CarCost.user_id == user_id)
        .order_by(CarCost.id.desc())
        .limit(limit)
        .all()
    )