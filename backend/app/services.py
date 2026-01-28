def calculate_repair_cost(car):
    current_year = 2026
    car_age = current_year - car.year
    base_repair_cost = 300 + (car_age * 150)
    km_factor = car.km_per_year / 15000 # 15.000 km/year = factor 1 
    risk_factor = car.repair_risk_factor

    annual_repairs = base_repair_cost * km_factor * risk_factor
    monthly_repairs = annual_repairs / 12

    return round(monthly_repairs, 2)

def calculate_costs(car):
    avg_consumption = 6.0 # liters per 100 km
    monthly_fuel_cost = (car.km_per_year / 100) * avg_consumption * car.fuel_price / 12
    estimated_repairs = 200 * car.repair_risk_factor / 12
    monthly_total = monthly_fuel_cost + estimated_repairs + car.insurance_cost + car.tax_cost

    monthly_repairs = calculate_repair_cost(car)

    return {
        "monthly_fuel_cost": round(monthly_fuel_cost, 2),
        "estimated_repairs": round(estimated_repairs, 2),
        "insurance_cost": round(car.insurance_cost, 2),
        "tax_cost": round(car.tax_cost, 2),
        "monthly_total_cost": round(monthly_total, 2),
        "note": "Estimare simplificată. Date reale pot varia."
    }
