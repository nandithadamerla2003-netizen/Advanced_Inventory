from fastapi import APIRouter
from database import cursor, db

router = APIRouter()

@router.post("/add-supplier")
def add_supplier(
        supplier_name: str,
        contact: str,
        location: str):

    cursor.execute(
        """
        INSERT INTO suppliers
        (supplier_name,contact,location)
        VALUES(%s,%s,%s)
        """,
        (supplier_name, contact, location)
    )

    db.commit()

    return {"message": "Supplier Added"}


@router.get("/suppliers")
def get_suppliers():

    cursor.execute("SELECT * FROM suppliers")

    return cursor.fetchall()