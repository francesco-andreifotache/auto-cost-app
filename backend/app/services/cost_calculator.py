from app.models import CarInput
from app.core.constants import FUEL_CONSUMPTION
from app.services.income_recommender import recommend_income
from app.services.fuel_price_service import get_fuel_price

def calculate_costs(car: CarInput) -> dict:
    fuel_price = get_fuel_price(car.fuel_type)

    fuel_data = FUEL_CONSUMPTION[car.fuel_type]

    annual_distance = car.km_per_year
    consumption = fuel_data["consumption_per_100km"]

    annual_energy_used = (annual_distance / 100) * consumption
    annual_fuel_cost = annual_energy_used * fuel_price

    monthly_fuel_cost = annual_fuel_cost / 12

    monthly_fixed_costs = car.insurance_cost + car.tax_cost

    repair_cost = monthly_fixed_costs * (car.repair_risk_factor - 1)

    total_monthly_cost = monthly_fuel_cost + monthly_fixed_costs + repair_cost

    income_recommendation = recommend_income(total_monthly_cost)

    return {
        "costs": {
            "fuel_type": car.fuel_type,
            "monthly_fuel_cost": round(monthly_fuel_cost, 2),
            "monthly_fixed_costs": round(monthly_fixed_costs, 2),
            "repair_risk_adjustment": round(repair_cost, 2),
            "total_monthly_cost": round(total_monthly_cost, 2),
            "currency": "RON"
        },
        "income_recommendation": income_recommendation
    }
