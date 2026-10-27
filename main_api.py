from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine

# Create the tables in the database (if they don't exist)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- 1. Database Dependency ---
# This function gives each request its own database session, then closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- 2. Data Models ---
class UserCreate(BaseModel):
    name: str
    age: int

# --- 3. API Endpoints ---

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    # This is the ORM magic: no SQL strings!
    users = db.query(models.User).all()
    return users

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Create a new Python object
    new_user = models.User(name=user.name, age=user.age)
    
    # Save it to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # Get the new ID from the database
    
    return {"message": "User created successfully", "user": new_user}