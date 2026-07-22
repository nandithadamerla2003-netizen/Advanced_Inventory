from fastapi import APIRouter, HTTPException

from schemas import ProductCreate
from database import insert_data, fetch_all, fetch_one

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/")
def add_product(product: ProductCreate):

    query = """
    INSERT INTO products
    (product_name, category, unit_price, supplier_id)
    VALUES (%s,%s,%s,%s)
    """

    values = (
        product.product_name,
        product.category,
        product.unit_price,
        product.supplier_id
    )

    insert_data(query, values)

    return {
        "message": "Product added successfully"
    }


@router.get("/")
def view_products():

    query = "SELECT * FROM products"

    products = fetch_all(query)

    return products


@router.get("/{product_id}")
def view_product(product_id: int):

    query = """
    SELECT * FROM products
    WHERE product_id=%s
    """

    product = fetch_one(query, (product_id,))

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product