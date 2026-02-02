from fastapi import APIRouter, HTTPException
from app.models import CarInput
from app.services.cost_calculator import calculate_costs
from fastapi import Depends
from app.core.auth import get_current_user
from sqlalchemy.orm import Session
from app.database.deps import get_db
from app.services.persist_cost import save_car_cost
from app.services.history_service import get_history
from app.database.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.models import UserCreate, UserLogin
from app.db_models.car_cost import CarCost
from app.utils.cost_calculator import calculate_annual_cost

router = APIRouter()

@router.get("/health", summary="Health Check")
async def health_check():
    return {"status": "ok"}

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user.email,
        password_hash=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_access_token({"sub": str(db_user.id)})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/calculate")
def calculate(
    car: CarInput,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    result = calculate_costs(car)

    save_car_cost(
        db=db,
        car=car,
        total_monthly_cost=result["costs"]["total_monthly_cost"],
        recommended_income=result["income_recommendation"]["safe_minimum_income"],
        user_id=user.id
    )

    return result

@router.get("/history")
def history(
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    records = get_history(db, user.id, limit)
    return records
