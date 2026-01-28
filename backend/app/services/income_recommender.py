from app.core.constants import SAFE_CAR_COST_PERCENTAGE, MAX_CAR_COST_PERCENTAGE

def recommend_income(monthly_car_cost: float) -> dict:
    safe_income = monthly_car_cost / SAFE_CAR_COST_PERCENTAGE
    max_income = monthly_car_cost / MAX_CAR_COST_PERCENTAGE

    return {
        "safe_minimum_income": round(safe_income, 2),
        "absolute_minimum_income": round(max_income, 2),
        "currency": "RON",
        "rules": {
            "safe_percentage": SAFE_CAR_COST_PERCENTAGE,
            "max_percentage": MAX_CAR_COST_PERCENTAGE
        }
    }