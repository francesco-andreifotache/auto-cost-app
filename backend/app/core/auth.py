from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from app.database.session import SessionLocal
# from app.database.models import User
from app.database.user import User

SECRET_KEY = "SECRET"
ALGORITHM = "HS256"

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    print(f"DEBUG: Token primit: {token[:10]}...") # Vedem daca ajunge tokenul

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"DEBUG: Payload decodat: {payload}") # Vedem daca trece de semnatura
        
        sub_value = payload.get("sub")
        if sub_value is None:
            print("DEBUG: Nu exista 'sub' in token")
            raise HTTPException(status_code=401, detail="Invalid token")
        user_id: str = str(sub_value)
        
    except JWTError as e:
        print(f"DEBUG: Eroare JWT: {e}") # Aici vedem daca e semnatura gresita
        raise HTTPException(status_code=401, detail="Invalid token")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
        print(f"DEBUG: User gasit in DB: {user}") # Vedem daca gaseste userul
    finally:
        db.close() # Inchidem conexiunea sigur

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user