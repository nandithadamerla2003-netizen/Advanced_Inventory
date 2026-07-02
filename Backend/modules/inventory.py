from fastapi import APIRouter
from database import cursor

router = APIRouter()

@router.get("/inventory")
def inventory():

    cursor.execute(
        """
        SELECT product_name,
               quantity,
               reorder_point
        FROM products
        """
    )

    return cursor.fetchall()


@router.get("/low-stock")
def low_stock():

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE quantity < reorder_point
        """
    )

    return cursor.fetchall()