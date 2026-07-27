from database import get_connection

connection = get_connection()

cursor = connection.cursor()

# Suppliers
cursor.execute("""

CREATE TABLE IF NOT EXISTS suppliers(

supplier_id INT AUTO_INCREMENT PRIMARY KEY,

supplier_name VARCHAR(100),

contact_person VARCHAR(100),

email VARCHAR(100),

phone VARCHAR(20),

address TEXT

)

""")

# Producs
cursor.execute("""

CREATE TABLE IF NOT EXISTS products(

product_id INT AUTO_INCREMENT PRIMARY KEY,

product_name VARCHAR(100),

category VARCHAR(50),

unit_price DECIMAL(10,2),

supplier_id INT,

FOREIGN KEY(supplier_id)

REFERENCES suppliers(supplier_id)

)

""")

# Inventory
cursor.execute("""

CREATE TABLE IF NOT EXISTS inventory(

inventory_id INT AUTO_INCREMENT PRIMARY KEY,

product_id INT,

quantity INT,

minimum_stock INT,

last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

FOREIGN KEY(product_id)

REFERENCES products(product_id)

)

""")

# Purchases
cursor.execute("""

CREATE TABLE IF NOT EXISTS purchases(

purchase_id INT AUTO_INCREMENT PRIMARY KEY,

product_id INT,

supplier_id INT,

quantity INT,

purchase_price DECIMAL(10,2),

purchase_date DATE,

FOREIGN KEY(product_id)

REFERENCES products(product_id),

FOREIGN KEY(supplier_id)

REFERENCES suppliers(supplier_id)

)

""")

# Sales
cursor.execute("""

CREATE TABLE IF NOT EXISTS sales(

sale_id INT AUTO_INCREMENT PRIMARY KEY,

product_id INT,

quantity INT,

selling_price DECIMAL(10,2),

sale_date DATE,

FOREIGN KEY(product_id)

REFERENCES products(product_id)

)

""")

# Users
cursor.execute("""
CREATE TABLE users (

    user_id INT AUTO_INCREMENT PRIMARY KEY,

    username VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    role VARCHAR(20) NOT NULL

);

""")

connection.commit()

cursor.close()

connection.close()

print("All tables created successfully.")

