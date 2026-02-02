from app.services.fuel_price_service import get_fuel_price

def calculate_annual_cost(car):
    avg_consumption = 7  # L / 100km (poți rafina ulterior)

    if car.fuel_type in ["petrol", "diesel"]:
        fuel_price = get_fuel_price(car.fuel_type)
        fuel_cost = (car.km_per_year / 100) * avg_consumption * fuel_price
    else:
        fuel_cost = 0  # electric / hybrid – separat mai târziu

    repair_cost = car.repair_risk_factor * (car.total_km / 10000) * 300

    total = (
        fuel_cost
        + car.insurance_cost
        + car.tax_cost
        + repair_cost
    )

    return {
        "fuel_cost": round(fuel_cost, 2),
        "repair_cost": round(repair_cost, 2),
        "total_annual_cost": round(total, 2)
    }
