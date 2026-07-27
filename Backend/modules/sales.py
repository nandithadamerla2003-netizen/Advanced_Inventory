from fastapi import APIRouter, HTTPException, Depends

from schemas import SaleCreate
from database import fetch_one, fetch_all, execute_transaction

from auth import verify_token, admin_required


router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)

# ADD
@router.post("/")
def add_sale(sale: SaleCreate,  user=Depends(admin_required)):

    inventory = fetch_one(
        "SELECT * FROM inventory WHERE product_id=%s",
        (sale.product_id,)
    )

    if inventory is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory record not found"
        )

    if inventory["quantity"] < sale.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    insert_sale = """
    INSERT INTO sales
    (product_id, quantity, selling_price)
    VALUES (%s,%s,%s)
    """

    update_inventory = """
    UPDATE inventory
    SET quantity = quantity - %s
    WHERE product_id=%s
    """

    execute_transaction([
        (
            insert_sale,
            (
                sale.product_id,
                sale.quantity,
                sale.selling_price
            )
        ),
        (
            update_inventory,
            (
                sale.quantity,
                sale.product_id
            )
        )
    ])

    return {
        "message": "Sale recorded successfully"
    }

# View All
@router.get("/")
def sales_history(user=Depends(verify_token)):

    query = """
    SELECT
        sales.sale_id,
        products.product_name,
        sales.quantity,
        sales.selling_price,
        sales.sale_date
    FROM sales
    JOIN products
    ON sales.product_id = products.product_id
    ORDER BY sale_date DESC
    """

    return fetch_all(query)