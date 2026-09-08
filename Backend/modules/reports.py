from fastapi import APIRouter, Depends
from database import fetch_all, fetch_one

from auth import verify_token


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

# Inventory Report

@router.get("/inventory")
def inventory_report(user=Depends(verify_token)):

    query = """
    SELECT
        i.inventory_id,
        p.product_name,
        p.category,
        i.quantity,
        i.minimum_stock
    FROM inventory i
    JOIN products p
        ON i.product_id = p.product_id
    """

    return fetch_all(query)

# Sales Report

@router.get("/sales")
def sales_report(user=Depends(verify_token)):

    query = """
    SELECT
        s.sale_id,
        p.product_name,
        s.quantity,
        s.selling_price,
        (s.quantity * s.selling_price) AS total_amount,
        s.sale_date
    FROM sales s
    JOIN products p
        ON s.product_id = p.product_id
    ORDER BY s.sale_date DESC
    """
    return fetch_all(query)

# Purchase Report

@router.get("/purchases")
def purchase_report(user=Depends(verify_token)):

    query = """
    SELECT
        pu.purchase_id,
        p.product_name,
        pu.quantity,
        pu.purchase_price,
        (pu.quantity * pu.purchase_price) AS total_amount,
        pu.purchase_date
    FROM purchases pu
    JOIN products p
        ON pu.product_id = p.product_id
    ORDER BY pu.purchase_date DESC
    """
    return fetch_all(query)

# Low Stock Report

@router.get("/low-stock")
def low_stock_report(user=Depends(verify_token)):

    query = """
    SELECT
        p.product_name,
        i.quantity,
        i.minimum_stock
    FROM inventory i
    JOIN products p
        ON i.product_id = p.product_id
    WHERE i.quantity <= i.minimum_stock
    """

    return fetch_all(query)

# Dashboard Summary

@router.get("/dashboard")
def dashboard_report(user=Depends(verify_token)):

    total_products = fetch_one(
        "SELECT COUNT(*) AS total FROM products",
        ()
    )

    total_suppliers = fetch_one(
        "SELECT COUNT(*) AS total FROM suppliers",
        ()
    )

    total_sales = fetch_one(
        """
        SELECT IFNULL(SUM(quantity * selling_price),0) AS total
        FROM sales
        """,
        ()
    )

    total_purchases = fetch_one(
        """
        SELECT IFNULL(SUM(quantity * purchase_price),0) AS total
        FROM purchases
        """,
        ()
    )

    low_stock = fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM inventory
        WHERE quantity <= minimum_stock
        """,
        ()
    )

    return {
        "total_products": total_products["total"],
        "total_suppliers": total_suppliers["total"],
        "total_sales_amount": float(total_sales["total"]),
        "total_purchase_amount": float(total_purchases["total"]),
        "low_stock_products": low_stock["total"]
    }