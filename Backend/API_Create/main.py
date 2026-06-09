from fastapi import FastAPI

from database import create_database
from create_sqltables import create_tables

app = FastAPI(
    title="Inventory Management System"
)

@app.on_event("startup")
def startup():

    create_database()

    create_tables()

    print("Database Ready")


@app.get("/")
def home():

    return {
        "message":
        "Inventory System Running"
    }