from database import get_connection

def get_products():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM products"
    )

    data = cursor.fetchall()

    conn.close()

    return data


def add_product(
        product_name,
        category,
        price,
        quantity,
        reorder_level,
        supplier_id
):

    conn = get_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO products
    (
        product_name,
        category,
        price,
        quantity,
        reorder_level,
        supplier_id
    )
    VALUES(%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(
        query,
        (
            product_name,
            category,
            price,
            quantity,
            reorder_level,
            supplier_id
        )
    )

    conn.commit()

    conn.close()