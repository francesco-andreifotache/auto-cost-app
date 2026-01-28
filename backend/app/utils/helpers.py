def confidence_level(car_age: int) -> str:
    if car_age < 3:
        return "High"
    elif 3 <= car_age <= 7:
        return "Medium"
    else:
        return "Low"