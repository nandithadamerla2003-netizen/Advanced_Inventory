from fastapi import APIRouter
from database import cursor, db

router = APIRouter()

@router.post("/add-product")
def add_product(
        sku_id: str,
        product_name: str,
        category: str,
        quantity: int,
        price: float,
        reorder_point: int):

    query = """
    INSERT INTO products
    (sku_id,product_name,category,quantity,price,reorder_point)
    VALUES(%s,%s,%s,%s,%s,%s)
    """

    values = (
        sku_id,
        product_name,
        category,
        quantity,
        price,
        reorder_point
    )

    cursor.execute(query, values)
    db.commit()

    return {"message": "Product Added"}


@router.get("/products")
def get_products():

    cursor.execute("SELECT * FROM products")

    return cursor.fetchall()


@router.delete("/delete-product/{id}")
def delete_product(id: int):

    cursor.execute(
        "DELETE FROM products WHERE id=%s",
        (id,)
    )

    db.commit()

    return {"message": "Deleted"}