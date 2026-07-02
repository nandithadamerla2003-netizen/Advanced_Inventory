from fastapi import APIRouter
from database import cursor, db

router = APIRouter()

@router.post("/add-sale")
def add_sale(
        product_name: str,
        quantity: int,
        total_price: float):

    cursor.execute(
        """
        INSERT INTO sales
        (product_name,quantity,total_price)
        VALUES(%s,%s,%s)
        """,
        (product_name, quantity, total_price)
    )

    cursor.execute(
        """
        UPDATE products
        SET quantity = quantity-%s
        WHERE product_name=%s
        """,
        (quantity, product_name)
    )

    db.commit()

    return {"message": "Sale Added"}