from database import get_connection

TABLES = {

    "suppliers": """
    CREATE TABLE IF NOT EXISTS suppliers(
        supplier_id INT AUTO_INCREMENT PRIMARY KEY,
        supplier_name VARCHAR(100) NOT NULL,
        phone VARCHAR(20),
        email VARCHAR(100),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """,

    "products": """
    CREATE TABLE IF NOT EXISTS products(
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        category VARCHAR(100),
        price DECIMAL(10,2),
        quantity INT DEFAULT 0,
        reorder_level INT DEFAULT 10,
        supplier_id INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
    )
    """,

    "purchases": """
    CREATE TABLE IF NOT EXISTS purchases(
        purchase_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        quantity INT,
        purchase_price DECIMAL(10,2),
        purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id)
        REFERENCES products(product_id)
    )
    """,

    "sales": """
    CREATE TABLE IF NOT EXISTS sales(
        sale_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        quantity INT,
        total_amount DECIMAL(10,2),
        sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(product_id)
        REFERENCES products(product_id)
    )
    """
}


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    for table_name, query in TABLES.items():

        try:

            cursor.execute(query)

            print(f"{table_name} table created")

        except Exception as error:

            print(
                f"Error creating {table_name}: {error}"
            )

    conn.commit()

    cursor.close()
    conn.close()