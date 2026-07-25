from fastapi import APIRouter, HTTPException

from schemas import PurchaseCreate
from database import fetch_one, fetch_all, execute_transaction

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"]
)

# ADD
@router.post("/")
def add_purchase(purchase: PurchaseCreate):

    product = fetch_one(
        "SELECT * FROM products WHERE product_id=%s",
        (purchase.product_id,)
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    insert_purchase = """
    INSERT INTO purchases
    (product_id, quantity, purchase_price)
    VALUES (%s,%s,%s)
    """

    update_inventory = """
    UPDATE inventory
    SET quantity = quantity + %s
    WHERE product_id=%s
    """

    execute_transaction([
        (
            insert_purchase,
            (
                purchase.product_id,
                purchase.quantity,
                purchase.purchase_price
            )
        ),
        (
            update_inventory,
            (
                purchase.quantity,
                purchase.product_id
            )
        )
    ])

    return {
        "message": "Purchase recorded successfully"
    }
# View All
@router.get("/")
def purchase_history():

    query = """
    SELECT
        purchases.purchase_id,
        products.product_name,
        purchases.quantity,
        purchases.purchase_price,
        purchases.purchase_date
    FROM purchases
    JOIN products
    ON purchases.product_id = products.product_id
    ORDER BY purchase_date DESC
    """

    return fetch_all(query)