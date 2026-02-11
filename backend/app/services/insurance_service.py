def estimate_rca(engine_cc: int, driver_age: int) -> float:
    """
    Estimează prețul RCA bazat pe motor și vârstă.
    Prețurile sunt aproximative pentru piața din România (Clasa B0).
    """
    base_price = 0

    # 1. Calcul bazat pe capacitatea cilindrică (CC)
    if engine_cc <= 1200:
        base_price = 800
    elif 1201 <= engine_cc <= 1400:
        base_price = 1000
    elif 1401 <= engine_cc <= 1600:
        base_price = 1200
    elif 1601 <= engine_cc <= 1800:
        base_price = 1400
    elif 1801 <= engine_cc <= 2000:
        base_price = 1600
    elif 2001 <= engine_cc <= 2500:
        base_price = 2200
    else:
        base_price = 3000  # Motoare foarte mari

    # 2. Factor de risc pentru vârstă
    # Dacă șoferul are sub 30 de ani, asigurarea e mai scumpă cu aprox 40%
    if driver_age < 30:
        base_price = base_price * 1.4

    return float(base_price)