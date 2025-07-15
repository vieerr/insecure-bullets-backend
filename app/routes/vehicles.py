from fastapi import APIRouter, HTTPException, Depends
import sqlite3
from app.database import get_db
from app.models import Item

router = APIRouter()

# 1. SQL Injection Vulnerability
@router.get("/sqli/{user_input}")
def sql_injection(user_input: str, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM items WHERE name = '{user_input}'")  # Deliberate SQLi
    return cursor.fetchall()

# 2. No Input Sanitization
@router.post("/create")
def create_unsafe(item: Item, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        f"INSERT INTO items (name, description, stock) VALUES "
        f"('{item.name}', '{item.description}', {item.stock})"
    )
    db.commit()
    return {"message": "Data injected unsafely"}

# 3. XSS Vulnerable Endpoint
@router.get("/xss")
def xss_vulnerable(name: str):
    return f"""
    <html>
        <body>
            <h1>Unsanitized Output: {name}</h1>  # XSS here
        </body>
    </html>
    """

# 4. Broken Authentication
@router.get("/admin")
def fake_admin(password: str):
    if password == "admin123":  # Hardcoded credentials
        return {"access": "granted"}
    return {"access": "denied"}