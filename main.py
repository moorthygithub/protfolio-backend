#poetry shell
#run using // uvicorn main:app --reload
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyodbc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=LAPTOP-BULFKGAE\\CM_SQL;'
    'DATABASE=PROFOLIO;'
    'Trusted_Connection=yes;'
)

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
except Exception as e:
    print(f"Database connection failed: {str(e)}")

class Profolio(BaseModel):
    Firstname: str
    Lastname: str
    Email: str
    Phone: str  
    Description: str



@app.post("/createprotfolio")
async def create_data(msg: Profolio):
    try:
        print(f"Received data: {msg.dict()}")  # Log data to check if it's coming

        sql = """
            INSERT INTO PROFOLIOS (Firstname, Lastname, Email, Phone, Description)
            VALUES (?, ?, ?, ?, ?)
        """
        cursor.execute(sql, (msg.Firstname, msg.Lastname, msg.Email, msg.Phone, msg.Description))
        conn.commit()

        return {"message": "Message sent successfully"}
    except Exception as e:
        return {"error": str(e)}


# Root Route (For Testing)
@app.get("/")
async def root():
    return {"message": "FastAPI backend is running"}
