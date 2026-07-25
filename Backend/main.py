from fastapi import FastAPI

from modules.suppliers import router as supplier_router
from modules.products import router as product_router
from modules.inventory import router as inventory_router
from modules.sales import router as sales_router
from modules.purchases import router as purchases_router
from modules.reports import router as reports_router

app = FastAPI(
    title="Advanced Inventory & Supplier Management System",
    version="1.0",
    
)


@app.get("/")
def home():

    return {
        "project": "Advanced Inventory & Supplier Management System",
        "status": "Running"
    }


@app.get("/health")
def health():

    return {
        "server": "Running",
        "database": "Configured"
    }



@app.get("/about")
def about():

    return {
        "developer": "Advanced Inventory Project",
        "framework": "FastAPI",
        "database": "MySQL"
    }

app.include_router(product_router)
app.include_router(supplier_router)
app.include_router(inventory_router)
app.include_router(sales_router)
app.include_router(purchases_router)
app.include_router(reports_router)