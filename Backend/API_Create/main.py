from fastapi import FastAPI

from modules.products import router as product_router
from modules.suppliers import router as supplier_router
from modules.inventory import router as inventory_router
from modules.sales import router as sales_router
from modules.purchases import router as purchases_router
from modules.reports import router as reports_router

app = FastAPI()

app.include_router(product_router)
app.include_router(supplier_router)
app.include_router(inventory_router)
app.include_router(sales_router)
app.include_router(purchases_router)
app.include_router(reports_router)


@app.get("/")
def home():
    return {"message": "Inventory System Running"}