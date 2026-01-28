from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class CarCost(Base):
    __tablename__ = "car_costs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    brand: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int]
    fuel_type: Mapped[str]

    km_per_year: Mapped[int]
    monthly_cost: Mapped[float]
    recommended_income: Mapped[float]

    user = relationship("User") 
