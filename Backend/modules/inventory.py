from fastapi import APIRouter, HTTPException

from schemas import InventoryCreate, InventoryUpdate
from database import insert_data, fetch_all, fetch_one, update_data

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

# ADD
@router.post("/")
def add_inventory(inventory: InventoryCreate):

    check_query = """
    SELECT * FROM products
    WHERE product_id=%s
    """

    product = fetch_one(check_query, (inventory.product_id,))

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    query = """
    INSERT INTO inventory
    (
        product_id,
        quantity,
        minimum_stock
    )
    VALUES
    (%s,%s,%s)
    """

    values = (
        inventory.product_id,
        inventory.quantity,
        inventory.minimum_stock
    )

    insert_data(query, values)

    return {
        "message": "Inventory added successfully"
    }

# View All
@router.get("/")
def view_inventory():

    query = """
    SELECT
        inventory.inventory_id,
        products.product_name,
        inventory.quantity,
        inventory.minimum_stock,
        inventory.last_updated
    FROM inventory
    JOIN products
    ON inventory.product_id = products.product_id
    """

    return fetch_all(query)

# Low Stock Checker API
@router.get("/low-stock")
def low_stock_items():

    query = """
    SELECT
        inventory.inventory_id,
        products.product_name,
        inventory.quantity,
        inventory.minimum_stock
    FROM inventory
    JOIN products
    ON inventory.product_id = products.product_id
    WHERE inventory.quantity <= inventory.minimum_stock
    """

    return fetch_all(query)

# Stock Alert API
@router.get("/alerts")
def stock_alerts():

    query = """
    SELECT
        products.product_name,
        inventory.quantity,
        inventory.minimum_stock
    FROM inventory
    JOIN products
    ON inventory.product_id=products.product_id
    WHERE inventory.quantity <= inventory.minimum_stock
    """

    items = fetch_all(query)

    if len(items) == 0:
        return {
            "message": "No low stock alerts"
        }

    return {
        "total_alerts": len(items),
        "items": items
    }

# Inventory Dashboard API
@router.get("/dashboard")
def inventory_dashboard():

    total_products = fetch_one(
        "SELECT COUNT(*) AS total FROM products",
        ()
    )

    total_inventory = fetch_one(
        "SELECT SUM(quantity) AS total_stock FROM inventory",
        ()
    )

    low_stock = fetch_one(
        """
        SELECT COUNT(*) AS low_stock
        FROM inventory
        WHERE quantity <= minimum_stock
        """,
        ()
    )

    return {
        "total_products": total_products["total"],
        "total_stock": total_inventory["total_stock"],
        "low_stock_items": low_stock["low_stock"]
    }

# View One
@router.get("/{inventory_id}")
def view_inventory_item(inventory_id: int):

    query = """
    SELECT
        inventory.inventory_id,
        products.product_name,
        inventory.quantity,
        inventory.minimum_stock,
        inventory.last_updated
    FROM inventory
    JOIN products
    ON inventory.product_id = products.product_id
    WHERE inventory.inventory_id=%s
    """

    inventory = fetch_one(query, (inventory_id,))

    if inventory is None:

        raise HTTPException(
            status_code=404,
            detail="Inventory not found"
        )

    return inventory

# Update
@router.put("/{inventory_id}")
def update_inventory(
    inventory_id: int,
    inventory: InventoryUpdate
):

    check_query = """
    SELECT *
    FROM inventory
    WHERE inventory_id=%s
    """

    existing = fetch_one(check_query, (inventory_id,))

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Inventory not found"
        )

    query = """
    UPDATE inventory
    SET
        quantity=%s,
        minimum_stock=%s
    WHERE inventory_id=%s
    """

    values = (
        inventory.quantity,
        inventory.minimum_stock,
        inventory_id
    )

    update_data(query, values)

    return {
        "message": "Inventory updated successfully"
    }

