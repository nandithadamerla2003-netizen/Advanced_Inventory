from database import get_connection

def low_stock():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute("""
    SELECT *
    FROM products
    WHERE quantity <= reorder_level
    """)

    data = cursor.fetchall()

    conn.close()

    return data