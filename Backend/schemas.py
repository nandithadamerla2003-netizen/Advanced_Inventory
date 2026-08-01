from pydantic import BaseModel, Field, EmailStr

# Suppliers
class SupplierCreate(BaseModel):
    supplier_name: str = Field(..., min_length=2, max_length=100)
    contact_person: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=5)


class SupplierResponse(BaseModel):
    supplier_id: int
    supplier_name: str
    contact_person: str
    email: str
    phone: str
    address: str

class SupplierUpdate(BaseModel):
    supplier_name: str = Field(..., min_length=2, max_length=100)
    contact_person: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    address: str = Field(..., min_length=5)



# Products

class ProductCreate(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    unit_price: float = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)

class ProductUpdate(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    unit_price: float = Field(..., gt=0)
    supplier_id: int = Field(..., gt=0)

class ProductResponse(BaseModel):
    product_id: int
    product_name: str
    category: str
    unit_price: float
    supplier_id: int

# Inventory
class InventoryCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    minimum_stock: int = Field(..., ge=0)


class InventoryUpdate(BaseModel):
    quantity: int = Field(..., ge=0)
    minimum_stock: int = Field(..., ge=0)

# Sales
class SaleCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    selling_price: float = Field(..., gt=0)


class SaleResponse(BaseModel):
    sale_id: int
    product_id: int
    quantity: int
    selling_price: float
    sale_date: str

# purchases
class PurchaseCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    purchase_price: float = Field(..., gt=0)

# Login Schema
class Login(BaseModel):
    Email: EmailStr
    username: str
    password: str

# Register Schema
class Register(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    Email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)