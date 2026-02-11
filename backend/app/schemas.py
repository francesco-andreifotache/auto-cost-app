from pydantic import BaseModel, Field, validator, EmailStr
from typing import Literal, Dict, Any

# --- USER ---
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Clasa ajutatoare pentru a arata costul dublu (Lunar si Anual)
class CostDetail(BaseModel):
    monthly: float
    annual: float

# --- MODELS PENTRU RASPUNS VENIT ---
# Asta defineste structura json-ului de venit pe care l-ai creat
class IncomeRules(BaseModel):
    safe_percentage: float
    max_percentage: float

class IncomeRecommendation(BaseModel):
    safe_minimum_income: float
    absolute_minimum_income: float
    currency: str
    rules: IncomeRules

# --- CARS ---
class CarInput(BaseModel):
    brand: str
    model: str
    fuel_type: Literal['petrol', 'diesel', 'electric', 'hybrid']
    year: int = Field(..., ge=1980, le=2026)
    km_per_year: int = Field(..., ge=0)
    fuel_consumption: float = Field(..., gt=0)
    engine_capacity: int = Field(..., ge=50, le=8000)
    driver_age: int = Field(..., ge=18, le=100)

    @validator('year')
    def year_not_in_future(cls, value):
        from datetime import datetime
        if value > datetime.now().year:
            raise ValueError('Anul nu poate fi in viitor')
        return value

class CarResponse(BaseModel):
    # Metadate
    id: int
    user_id: int
    
    # Datele Masinii (le copiem manual in raspuns sau folosim inheritance, 
    # dar aici e mai clar sa le definim explicit pentru structura noua)
    brand: str
    model: str
    year: int
    
    # COSTURILE REORGANIZATE
    fuel: CostDetail
    insurance: CostDetail
    maintenance: CostDetail
    total: CostDetail
    
    # Venit
    income_analysis: IncomeRecommendation # Asigura-te ca ai importat clasa asta din codul anterior

    class Config:
        from_attributes = True