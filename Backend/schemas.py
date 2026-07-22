from pydantic import BaseModel, Field

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

# Products

class ProductCreate(BaseModel):
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

    