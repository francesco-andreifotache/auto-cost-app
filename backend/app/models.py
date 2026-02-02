from pydantic import BaseModel, Field, validator
from typing import Literal
from datetime import datetime

class CarInput(BaseModel):
    brand: str
    model: str

    fuel_type: Literal['petrol', 'diesel', 'electric', 'hybrid']

    year: int = Field(..., ge=1980, le=2026)
    km_per_year: int = Field(..., ge=0)
    total_km: int = Field(..., ge=0)
    # fuel_price: float = Field(..., ge=0) 
    insurance_cost: float = Field(..., ge=0)
    tax_cost: float = Field(..., ge=0)
    repair_risk_factor: float = Field(1, ge=0.5, le=2.0)

    @ validator('year')
    def year_not_in_future(cls, value):
        if value > datetime.now().year:
            raise ValueError('Year cannot be in the future')
        return value
    
class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str