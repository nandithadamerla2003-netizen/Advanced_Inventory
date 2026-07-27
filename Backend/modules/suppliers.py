from fastapi import APIRouter, HTTPException, Depends

from schemas import SupplierCreate, SupplierUpdate
from database import insert_data, fetch_all, fetch_one, update_data, delete_data

from auth import verify_token, admin_required


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)

# ADD
@router.post("/")
def add_supplier(supplier: SupplierCreate, user=Depends(admin_required)):

    query = """
    INSERT INTO suppliers
    (
        supplier_name,
        contact_person,
        email,
        phone,
        address
    )
    VALUES
    (%s,%s,%s,%s,%s)
    """

    values = (
        supplier.supplier_name,
        supplier.contact_person,
        supplier.email,
        supplier.phone,
        supplier.address
    )

    insert_data(query, values)

    return {
        "message": "Supplier added successfully"
    }

# View All
@router.get("/")
def view_suppliers(user=Depends(verify_token)):

    query = """
    SELECT * FROM suppliers
    """

    suppliers = fetch_all(query)

    return suppliers

# View One
@router.get("/{supplier_id}")
def view_supplier(supplier_id: int, user=Depends(verify_token)):

    query = """
    SELECT *
    FROM suppliers
    WHERE supplier_id=%s
    """

    supplier = fetch_one(query, (supplier_id,))

    if supplier is None:

        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    return supplier

# Update
@router.put("/{supplier_id}")
def update_supplier(supplier_id: int, supplier: SupplierUpdate, user=Depends(admin_required)):

    check_query = """
    SELECT *
    FROM suppliers
    WHERE supplier_id=%s
    """

    existing_supplier = fetch_one(check_query, (supplier_id,))

    if existing_supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    query = """
    UPDATE suppliers
    SET
        supplier_name=%s,
        contact_person=%s,
        email=%s,
        phone=%s,
        address=%s
    WHERE supplier_id=%s
    """

    values = (
        supplier.supplier_name,
        supplier.contact_person,
        supplier.email,
        supplier.phone,
        supplier.address,
        supplier_id
    )

    update_data(query, values)

    return {
        "message": "Supplier updated successfully"
    }

# Delete

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, user=Depends(admin_required)):

    check_query = """
    SELECT *
    FROM suppliers
    WHERE supplier_id=%s
    """

    existing_supplier = fetch_one(check_query, (supplier_id,))

    if existing_supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found"
        )

    query = """
    DELETE FROM suppliers
    WHERE supplier_id=%s
    """

    delete_data(query, (supplier_id,))

    return {
        "message": "Supplier deleted successfully"
    }