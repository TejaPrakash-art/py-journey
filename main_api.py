from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import models
from database import SessionLocal, engine
from auth import get_password_hash, verify_password, create_access_token, SECRET_KEY, ALGORITHM

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# This tells FastAPI where the login route is
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Data Models ---
class UserCreate(BaseModel):
    name: str
    age: int
    password: str

# --- API Endpoints ---

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Hash the password
    hashed_pw = get_password_hash(user.password)
    
    # 2. Save to database
    new_user = models.User(name=user.name, age=user.age, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "user_id": new_user.id}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Find user by name (OAuth2 uses 'username' field, we'll treat it as our 'name')
    user = db.query(models.User).filter(models.User.name == form_data.username).first()
    
    # 2. Check if user exists AND password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    # 3. Create and return the token
    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # This function runs when a user provides a token. It decodes the token.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.name == username).first()
    if user is None:
        raise credentials_exception
    return {"message": f"Hello {user.name}, you are seeing this because you are logged in!", "age": user.age}