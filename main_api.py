from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# --- 1. Database Setup ---
def get_db():
    # Connect to the same database we created in the SQL lesson
    return sqlite3.connect("test.db")

# --- 2. Data Models ---
# This tells FastAPI exactly what data to expect when a user is created
class UserCreate(BaseModel):
    name: str
    age: int

# --- 3. API Endpoints ---

@app.get("/users")
def get_users():
    conn = get_db()
    # row_factory lets us access columns by name (e.g., user['name']) instead of index (user[1])
    conn.row_factory = sqlite3.Row
    cursor = conn.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    
    # Convert the database rows to a list of dictionaries for JSON
    return [dict(u) for u in users]

@app.post("/users")
def create_user(user: UserCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO users (name, age) VALUES (?, ?)", 
        (user.name, user.age)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    
    return {"message": "User created successfully", "id": new_id, "name": user.name}