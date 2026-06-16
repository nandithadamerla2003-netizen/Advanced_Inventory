from fastapi import APIRouter
from database import cursor, db

router = APIRouter()

@router.post("/add-purchase")
def add_purchase(
        product_name: str,
        quantity: int,
        purchase_price: float):

    cursor.execute(
        """
        INSERT INTO purchases
        (product_name,quantity,purchase_price)
        VALUES(%s,%s,%s)
        """,
        (product_name, quantity, purchase_price)
    )

    cursor.execute(
        """
        UPDATE products
        SET quantity = quantity+%s
        WHERE product_name=%s
        """,
        (quantity, product_name)
    )

    db.commit()

    return {"message": "Purchase Added"}