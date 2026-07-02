from database import cursor, db

cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
id INT AUTO_INCREMENT PRIMARY KEY,
sku_id VARCHAR(50),
product_name VARCHAR(100),
category VARCHAR(50),
quantity INT,
price FLOAT,
reorder_point INT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers(
id INT AUTO_INCREMENT PRIMARY KEY,
supplier_name VARCHAR(100),
contact VARCHAR(20),
location VARCHAR(100)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sales(
id INT AUTO_INCREMENT PRIMARY KEY,
product_name VARCHAR(100),
quantity INT,
total_price FLOAT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS purchases(
id INT AUTO_INCREMENT PRIMARY KEY,
product_name VARCHAR(100),
quantity INT,
purchase_price FLOAT
)
""")

db.commit()

print("Tables Created")