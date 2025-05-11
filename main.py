# #poetry shell
# #run using // uvicorn main:app --reload
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import pyodbc

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_credentials=True,
#     allow_methods=["*"], 
#     allow_headers=["*"],  
# )

# conn_str = (
#     'DRIVER={ODBC Driver 17 for SQL Server};'
#     'SERVER=LAPTOP-BULFKGAE\\CM_SQL;'
#     'DATABASE=PROFOLIO;'
#     'Trusted_Connection=yes;'
# )

# try:
#     conn = pyodbc.connect(conn_str)
#     cursor = conn.cursor()
# except Exception as e:
#     print(f"Database connection failed: {str(e)}")

# class Profolio(BaseModel):
#     Firstname: str
#     Lastname: str
#     Email: str
#     Phone: str  
#     Description: str



# @app.post("/createprotfolio")
# async def create_data(msg: Profolio):
#     try:
#         print(f"Received data: {msg.dict()}")  # Log data to check if it's coming

#         sql = """
#             INSERT INTO PROFOLIOS (Firstname, Lastname, Email, Phone, Description)
#             VALUES (?, ?, ?, ?, ?)
#         """
#         cursor.execute(sql, (msg.Firstname, msg.Lastname, msg.Email, msg.Phone, msg.Description))
#         conn.commit()

#         return {"message": "Message sent successfully"}
#     except Exception as e:
#         return {"error": str(e)}


# # Root Route (For Testing)
# @app.get("/")
# async def root():
#     return {"message": "FastAPI backend is running"}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

# ----------------------
# FastAPI Initialization
# ----------------------
app = FastAPI()

# ----------------------
# CORS Middleware
# ----------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# Database Setup (SQLite)
# ----------------------
db_path = os.path.join(os.path.dirname(__file__), "data.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS PROFOLIOS (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Firstname TEXT,
        Lastname TEXT,
        Email TEXT,
        Phone TEXT,
        Description TEXT
    )
''')
conn.commit()

# ----------------------
# Pydantic Model
# ----------------------
class Profolio(BaseModel):
    Firstname: str
    Lastname: str
    Email: str
    Phone: str
    Description: str

# ----------------------
# API Endpoints
# ----------------------

@app.post("/createportfolio")
async def create_data(msg: Profolio):
    try:
        cursor.execute('''
            INSERT INTO PROFOLIOS (Firstname, Lastname, Email, Phone, Description)
            VALUES (?, ?, ?, ?, ?)
        ''', (msg.Firstname, msg.Lastname, msg.Email, msg.Phone, msg.Description))
        conn.commit()
        return {"message": "Portfolio data saved successfully"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    return {"message": "FastAPI backend with SQLite is running"}

# Optional: Run app directly with `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
