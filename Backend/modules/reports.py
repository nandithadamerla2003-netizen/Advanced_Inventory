from database import get_connection

def inventory_report():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
    SELECT
        product_name,
        quantity,
        price
    FROM products
    """)

    data = cursor.fetchall()

    conn.close()

    return data