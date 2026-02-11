from app.schemas import CarInput
from app.services.fuel_price_service import get_fuel_price
from app.services.insurance_service import estimate_rca
from app.services.income_recommender import recommend_income # <--- Importam functia ta
from datetime import datetime

PREMIUM_BRANDS = ["bmw", "mercedes", "audi", "porsche", "lexus", "land rover", "jaguar", "volvo"]

def _calculate_risk_factor(brand: str, year: int, km_per_year: int) -> float:
    factor = 1.0
    current_year = datetime.now().year
    car_age = current_year - year

    if brand.lower() in PREMIUM_BRANDS: factor += 0.5
    
    if car_age > 10: factor += 0.4
    elif car_age > 5: factor += 0.2

    if km_per_year > 25000: factor += 0.3
    elif km_per_year > 15000: factor += 0.1

    return round(factor, 2)

def calculate_costs(car_data: CarInput) -> dict:
    # 1. Calcule Standard
    fuel_price = get_fuel_price(car_data.fuel_type)
    liters_needed = (car_data.km_per_year / 100) * car_data.fuel_consumption
    annual_fuel_cost = liters_needed * fuel_price

    insurance_cost = estimate_rca(car_data.engine_capacity, car_data.driver_age)

    risk_factor = _calculate_risk_factor(car_data.brand, car_data.year, car_data.km_per_year)
    base_maintenance = 1200 
    maintenance_cost = base_maintenance * risk_factor

    total_annual_cost = annual_fuel_cost + insurance_cost + maintenance_cost

    # 2. Integrarea functiei tale pentru Venit
    monthly_cost = total_annual_cost / 12
    
    # Aici apelam functia ta exact cum ai scris-o
    income_data = recommend_income(monthly_cost)

    return {
        "annual_fuel_cost": round(annual_fuel_cost, 2),
        "insurance_cost": round(insurance_cost, 2),
        "maintenance_cost": round(maintenance_cost, 2),
        "total_annual_cost": round(total_annual_cost, 2),
        "repair_risk_factor": risk_factor,
        "income_analysis": income_data # Trimitem tot obiectul complex mai departe
    }