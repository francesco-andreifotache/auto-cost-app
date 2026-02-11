from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import CarInput, CarResponse, UserCreate, UserLogin, Token
from app.database.deps import get_db
from app.database.user import User
from app.database.car import Car
from app.services.cost_calculator import calculate_costs
from app.services.income_recommender import recommend_income # Importam pentru istoric
from app.core.auth import get_current_user
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter()

# ... (LOGIN / REGISTER raman la fel, nu le mai scriu aici) ...
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing: raise HTTPException(status_code=400, detail="Email exists")
    new_user = User(email=user.email, password_hash=hash_password(user.password))
    db.add(new_user)
    db.commit()
    return {"message": "User registered"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Bad credentials")
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer" }


@router.post("/calculate", response_model=CarResponse)
def calculate(
    car_input: CarInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Calculăm
    results = calculate_costs(car_input)

    # 2. Salvăm în DB (În DB salvăm doar valorile anuale, e cel mai eficient)
    safe_income_value = results["income_analysis"]["safe_minimum_income"]

    new_entry = Car(
        user_id=current_user.id,
        brand=car_input.brand,
        model=car_input.model,
        year=car_input.year,
        fuel_type=car_input.fuel_type,
        fuel_consumption=car_input.fuel_consumption,
        km_per_year=car_input.km_per_year,
        engine_capacity=car_input.engine_capacity,
        driver_age=car_input.driver_age,
        
        repair_risk_factor=results["repair_risk_factor"],
        annual_fuel_cost=results["annual_fuel_cost"],
        insurance_cost=results["insurance_cost"],
        maintenance_cost=results["maintenance_cost"],
        total_annual_cost=results["total_annual_cost"],
        recommended_income=safe_income_value 
    )
    
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    # 3. Construim Răspunsul Structurat (Annual vs Monthly)
    # Aici facem conversia pentru afișare
    return {
        "id": new_entry.id,
        "user_id": new_entry.user_id,
        "brand": new_entry.brand,
        "model": new_entry.model,
        "year": new_entry.year,
        
        "fuel": {
            "annual": new_entry.annual_fuel_cost,
            "monthly": round(new_entry.annual_fuel_cost / 12, 2)
        },
        "insurance": {
            "annual": new_entry.insurance_cost,
            "monthly": round(new_entry.insurance_cost / 12, 2)
        },
        "maintenance": {
            "annual": new_entry.maintenance_cost,
            "monthly": round(new_entry.maintenance_cost / 12, 2)
        },
        "total": {
            "annual": new_entry.total_annual_cost,
            "monthly": round(new_entry.total_annual_cost / 12, 2)
        },
        
        "income_analysis": results["income_analysis"]
    }

@router.get("/history", response_model=List[CarResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_records = db.query(Car).filter(Car.user_id == current_user.id).order_by(Car.created_at.desc()).all()
    
    history_response = []
    for record in db_records:
        # Recalculăm income analysis pentru istoric
        monthly_total = record.total_annual_cost / 12
        income_data = recommend_income(monthly_total)
        
        # Construim structura detaliată
        record_dict = {
            "id": record.id,
            "user_id": record.user_id,
            "brand": record.brand,
            "model": record.model,
            "year": record.year,
            
            "fuel": {
                "annual": record.annual_fuel_cost,
                "monthly": round(record.annual_fuel_cost / 12, 2)
            },
            "insurance": {
                "annual": record.insurance_cost,
                "monthly": round(record.insurance_cost / 12, 2)
            },
            "maintenance": {
                "annual": record.maintenance_cost,
                "monthly": round(record.maintenance_cost / 12, 2)
            },
            "total": {
                "annual": record.total_annual_cost,
                "monthly": round(record.total_annual_cost / 12, 2)
            },
            
            "income_analysis": income_data
        }
        history_response.append(record_dict)
        
    return history_response