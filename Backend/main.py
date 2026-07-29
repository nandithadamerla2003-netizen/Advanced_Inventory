from fastapi import FastAPI, Request

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from modules.auth_routes import router as auth_router
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

# Mount the Static Folder
app.mount(
    "/static",
    StaticFiles(directory="../Frontend/static"),
    name="static"
)

# Configure the Templates Folder
templates = Jinja2Templates(
    directory="../Frontend/templates"
)

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )

# Health API
@app.get("/health")
def health():

    return {
        "server": "Running",
        "database": "Configured"
    }


# About API
@app.get("/about")
def about():

    return {
        "developer": "Advanced Inventory Project",
        "framework": "FastAPI",
        "database": "MySQL"
    }

# Dashboard
@app.get("/dashboard")
def dashboard(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request
        }
    )

# Products
@app.get("/products-page")
def products_page(request: Request):

    return templates.TemplateResponse(
        "products.html",
        {
            "request": request
        }
    )

# Suppliers
@app.get("/suppliers-page")
def suppliers_page(request: Request):

    return templates.TemplateResponse(
        "suppliers.html",
        {
            "request": request
        }
    )

# Inventory
@app.get("/inventory-page")
def inventory_page(request: Request):

    return templates.TemplateResponse(
        "inventory.html",
        {
            "request": request
        }
    )

# Sales
@app.get("/sales-page")
def sales_page(request: Request):

    return templates.TemplateResponse(
        "sales.html",
        {
            "request": request
        }
    )

# Reports
@app.get("/reports-page")
def reports_page(request: Request):

    return templates.TemplateResponse(
        "reports.html",
        {
            "request": request
        }
    )

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(supplier_router)
app.include_router(inventory_router)
app.include_router(sales_router)
app.include_router(purchases_router)
app.include_router(reports_router)