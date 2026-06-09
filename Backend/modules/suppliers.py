from database import get_connection

def get_suppliers():

    conn = get_connection()

    cursor = conn.cursor(
        dictionary=True
    )

    cursor.execute(
        "SELECT * FROM suppliers"
    )

    data = cursor.fetchall()

    conn.close()

    return data


def add_supplier(
        supplier_name,
        phone,
        email
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO suppliers
    (
        supplier_name,
        phone,
        email
    )
    VALUES(%s,%s,%s)
    """,
    (
        supplier_name,
        phone,
        email
    ))

    conn.commit()

    conn.close()