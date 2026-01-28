from sqlalchemy.orm import Session
from app.db_models.car_cost import CarCost
from app.models import CarInput

def save_car_cost(
    db: Session,
    car: CarInput,
    total_monthly_cost: float,
    recommended_income: float,
    user_id: int
):
    entry = CarCost(
        brand=car.brand,
        model=car.model,
        year=car.year,
        fuel_type=car.fuel_type,
        km_per_year=car.km_per_year,
        monthly_cost=total_monthly_cost,
        recommended_income=recommended_income,
        user_id=user_id
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry
