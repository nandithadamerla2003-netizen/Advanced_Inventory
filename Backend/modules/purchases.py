from database import get_connection

def add_stock(
        product_id,
        quantity
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE products
    SET quantity = quantity + %s
    WHERE product_id = %s
    """,
    (
        quantity,
        product_id
    ))

    conn.commit()

    conn.close()