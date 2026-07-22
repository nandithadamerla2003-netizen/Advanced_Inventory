from fastapi import APIRouter, HTTPException

from schemas import ProductCreate, ProductUpdate
from database import insert_data, fetch_all, fetch_one, update_data, delete_data

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

# ADD
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

# View All
@router.get("/")
def view_products():

    query = "SELECT * FROM products"

    products = fetch_all(query)

    return products

# View One
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

# Update

@router.put("/{product_id}")
def update_product(product_id: int, product: ProductUpdate):

    check_query = "SELECT * FROM products WHERE product_id=%s"

    existing_product = fetch_one(check_query, (product_id,))

    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    query = """
    UPDATE products
    SET
        product_name=%s,
        category=%s,
        unit_price=%s,
        supplier_id=%s
    WHERE product_id=%s
    """

    values = (
        product.product_name,
        product.category,
        product.unit_price,
        product.supplier_id,
        product_id
    )

    update_data(query, values)

    return {
        "message": "Product updated successfully"
    }

# Delete

@router.delete("/{product_id}")
def delete_product(product_id: int):

    check_query = "SELECT * FROM products WHERE product_id=%s"

    existing_product = fetch_one(check_query, (product_id,))

    if existing_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    query = "DELETE FROM products WHERE product_id=%s"

    delete_data(query, (product_id,))

    return {
        "message": "Product deleted successfully"
    }