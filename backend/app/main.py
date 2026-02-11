from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- Aici era greșeala
from app.routes import router
from app.database.session import engine
from app.database.base import Base
# Asigură-te că modelele sunt importate pentru a fi create în DB
from app.db_models import car_cost
from app.database.car import Car
from app.database.user import User

# Configurare CORS (Permite Frontend-ului să vorbească cu Backend-ul)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app = FastAPI(
    title="Auto Cost Calculator API",
    description="Estimare costuri reale de întreținere auto pe baza datelor introduse de utilizator.",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite toate metodele (GET, POST etc.)
    allow_headers=["*"], # Permite toate headerele
)

# Crearea tabelelor în baza de date (dacă nu există)
Base.metadata.create_all(bind=engine)

# Includerea rutelor
app.include_router(router)