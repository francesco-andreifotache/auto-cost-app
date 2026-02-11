from sqlalchemy import String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from app.database.base import Base
from datetime import datetime

class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # --- INPUTS (Date introduse) ---
    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int] = mapped_column(Integer)
    fuel_type: Mapped[str] = mapped_column(String(20))
    fuel_consumption: Mapped[float] = mapped_column(Float)
    km_per_year: Mapped[int] = mapped_column(Integer)
    engine_capacity: Mapped[int] = mapped_column(Integer)
    driver_age: Mapped[int] = mapped_column(Integer)

    # --- OUTPUTS (Rezultate calculate pe care le salvăm) ---
    # Python nu le găsea pe acestea:
    repair_risk_factor: Mapped[float] = mapped_column(Float, default=1.0)
    annual_fuel_cost: Mapped[float] = mapped_column(Float, default=0.0)
    insurance_cost: Mapped[float] = mapped_column(Float, default=0.0)
    maintenance_cost: Mapped[float] = mapped_column(Float, default=0.0)
    total_annual_cost: Mapped[float] = mapped_column(Float, default=0.0)
    
    # Coloana pentru venitul recomandat (Safe Income)
    recommended_income: Mapped[float] = mapped_column(Float, default=0.0)

    # Data creării
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())