from fastapi import FastAPI
from app.routes import router
from app.database.session import engine
from app.database.base import Base
from app.db_models import car_cost

app = FastAPI(
    title="Auto Cost Calculator API",
    description="Estimare costuri reale de întreținere auto pe baza datelor introduse de utilizator.",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(router)
