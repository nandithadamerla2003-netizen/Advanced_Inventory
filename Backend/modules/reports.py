from fastapi import APIRouter
from database import cursor

router = APIRouter()

@router.get("/inventory-value")
def inventory_value():

    cursor.execute(
        """
        SELECT SUM(quantity*price)
        FROM products
        """
    )

    result = cursor.fetchone()

    return {
        "Inventory Value": result[0]
    }