/* =========================================================
   1. API CONFIGURATION
   ========================================================= */

const BASE_URL = "http://127.0.0.1:8000";


/* =========================================================
   2. JWT TOKEN FUNCTIONS
   ========================================================= */

function getToken() {

    return localStorage.getItem("access_token");

}


function saveToken(token) {

    localStorage.setItem(
        "access_token",
        token
    );

}


function removeToken() {

    localStorage.removeItem(
        "access_token"
    );

}


/* =========================================================
   3. ERROR MESSAGE
   ========================================================= */

function getErrorMessage(data) {

    if (!data) {

        return "Request failed.";

    }


    if (Array.isArray(data.detail)) {

        return data.detail
            .map(error => {

                const location =
                    error.loc
                        ? error.loc.join(".")
                        : "field";

                return (
                    location +
                    ": " +
                    error.msg
                );

            })
            .join("\n");

    }


    return (
        data.detail ||
        data.message ||
        "Request failed."
    );

}


/* =========================================================
   4. LOGOUT
   ========================================================= */

function logout() {

    removeToken();

    alert(
        "Logged out successfully."
    );

    window.location.href =
        "index.html";

}


/* =========================================================
   5. LOGIN
   ========================================================= */

async function login(
    Email,
    username,
    password
) {

    try {

        const response =
            await fetch(
                BASE_URL + "/auth/login",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            Email:
                                Email,

                            username:
                                username,

                            password:
                                password

                        })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                getErrorMessage(data)
            );

            return false;

        }


        saveToken(
            data.access_token
        );


        alert(
            "Login successful."
        );


        window.location.href =
            "dashboard.html";


        return true;


    } catch (error) {

        console.error(
            "Login Error:",
            error
        );

        alert(
            "Unable to connect to server."
        );

        return false;

    }

}


/* =========================================================
   6. REGISTRATION
   ========================================================= */

async function register(
    full_name,
    Email,
    username,
    password
) {

    try {

        const response =
            await fetch(
                BASE_URL + "/auth/register",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            full_name:
                                full_name,

                            Email:
                                Email,

                            username:
                                username,

                            password:
                                password

                        })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                getErrorMessage(data)
            );

            return false;

        }


        alert(
            "Registration successful. Please login."
        );


        window.location.href =
            "login.html";


        return true;


    } catch (error) {

        console.error(
            "Registration Error:",
            error
        );

        alert(
            "Unable to connect to server."
        );

        return false;

    }

}


/* =========================================================
   7. GET CURRENT USER
   ========================================================= */

async function getCurrentUser() {

    const token =
        getToken();


    if (!token) {

        return null;

    }


    try {

        const response =
            await fetch(
                BASE_URL + "/auth/me",
                {

                    method: "GET",

                    headers: {

                        "Authorization":
                            "Bearer " + token

                    }

                }
            );


        if (!response.ok) {

            return null;

        }


        return await response.json();


    } catch (error) {

        console.error(
            "Current User Error:",
            error
        );

        return null;

    }

}


/* =========================================================
   8. CHECK LOGIN
   ========================================================= */

async function checkLogin() {

    const token =
        getToken();


    if (!token) {

        alert(
            "Please login first."
        );

        window.location.href =
            "login.html";

        return null;

    }


    const user =
        await getCurrentUser();


    if (!user) {

        removeToken();

        alert(
            "Session expired. Please login again."
        );

        window.location.href =
            "login.html";

        return null;

    }


    return user;

}


/* =========================================================
   9. ROLE BASED UI
   ========================================================= */

function applyRoleBasedUI(user) {

    if (!user) {

        return;

    }


    /* Username */

    const usernameElements =
        document.querySelectorAll(
            "#currentUsername, .current-username"
        );


    usernameElements.forEach(
        element => {

            element.innerText =
                user.username || "-";

        }
    );


    /* Role */

    const roleElements =
        document.querySelectorAll(
            "#currentRole, .current-role"
        );


    roleElements.forEach(
        element => {

            element.innerText =
                user.role || "User";

        }
    );


    /* Admin-only elements */

    const adminElements =
        document.querySelectorAll(
            ".admin-only"
        );


    adminElements.forEach(
        element => {

            if (
                user.role === "Admin"
            ) {

                element.style.display =
                    "";

            } else {

                element.style.display =
                    "none";

            }

        }
    );

}


/* =========================================================
   10. GENERIC GET REQUEST
   ========================================================= */

async function fetchData(endpoint) {

    try {

        const token =
            getToken();


        const headers = {};


        if (token) {

            headers["Authorization"] =
                "Bearer " + token;

        }


        const response =
            await fetch(
                BASE_URL + endpoint,
                {

                    method: "GET",

                    headers:
                        headers

                }
            );


        if (
            response.status ===
            401
        ) {

            removeToken();

            alert(
                "Session expired. Please login again."
            );

            window.location.href =
                "login.html";

            return null;

        }


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                getErrorMessage(data)
            );

            return null;

        }


        return data;


    } catch (error) {

        console.error(
            "GET Error:",
            error
        );

        alert(
            "Unable to connect to backend."
        );

        return null;

    }

}


/* =========================================================
   11. GENERIC POST REQUEST
   ========================================================= */

async function postData(
    endpoint,
    body
) {

    try {

        const token =
            getToken();


        const headers = {

            "Content-Type":
                "application/json"

        };


        if (token) {

            headers["Authorization"] =
                "Bearer " + token;

        }


        const response =
            await fetch(
                BASE_URL + endpoint,
                {

                    method: "POST",

                    headers:
                        headers,

                    body:
                        JSON.stringify(body)

                }
            );


        if (
            response.status ===
            401
        ) {

            removeToken();

            alert(
                "Session expired. Please login again."
            );

            window.location.href =
                "login.html";

            return null;

        }


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                getErrorMessage(data)
            );

            return null;

        }


        return data;


    } catch (error) {

        console.error(
            "POST Error:",
            error
        );

        alert(
            "Unable to connect to backend."
        );

        return null;

    }

}


/* =========================================================
   12. GENERIC PUT REQUEST
   ========================================================= */

async function putData(
    endpoint,
    body
) {

    try {

        const token =
            getToken();


        const response =
            await fetch(
                BASE_URL + endpoint,
                {

                    method: "PUT",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Authorization":
                            "Bearer " + token

                    },

                    body:
                        JSON.stringify(body)

                }
            );


        if (
            response.status ===
            401
        ) {

            removeToken();

            alert(
                "Session expired. Please login again."
            );

            window.location.href =
                "login.html";

            return null;

        }


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                getErrorMessage(data)
            );

            return null;

        }


        return data;


    } catch (error) {

        console.error(
            "PUT Error:",
            error
        );

        alert(
            "Unable to connect to backend."
        );

        return null;

    }

}


/* =========================================================
   13. GENERIC DELETE REQUEST
   ========================================================= */

async function deleteData(
    endpoint
) {

    try {

        const token =
            getToken();


        const response =
            await fetch(
                BASE_URL + endpoint,
                {

                    method: "DELETE",

                    headers: {

                        "Authorization":
                            "Bearer " + token

                    }

                }
            );


        if (
            response.status ===
            401
        ) {

            removeToken();

            alert(
                "Session expired. Please login again."
            );

            window.location.href =
                "login.html";

            return null;

        }


        const data =
            await response.json();


        if (!response.ok) {

            alert(
                getErrorMessage(data)
            );

            return null;

        }


        return data;


    } catch (error) {

        console.error(
            "DELETE Error:",
            error
        );

        alert(
            "Unable to connect to backend."
        );

        return null;

    }

}


/* =========================================================
   14. LOAD GENERIC TABLE
   ========================================================= */

function loadTable(
    data,
    tbodyId,
    columns
) {

    const tbody =
        document.getElementById(
            tbodyId
        );


    if (!tbody) {

        return;

    }


    tbody.innerHTML = "";


    if (
        !data ||
        data.length === 0
    ) {

        tbody.innerHTML = `

            <tr>

                <td colspan="${columns.length}">

                    No records found.

                </td>

            </tr>

        `;

        return;

    }


    data.forEach(
        item => {

            let row =
                "<tr>";


            columns.forEach(
                column => {

                    row += `

                        <td>

                            ${item[column] ?? "-"}

                        </td>

                    `;

                }
            );


            row +=
                "</tr>";


            tbody.innerHTML +=
                row;

        }
    );

}


/* =========================================================
   15. SUBMIT FORM
   ========================================================= */

async function submitForm(
    formId,
    endpoint
) {

    const form =
        document.getElementById(
            formId
        );


    if (!form) {

        return;

    }


    const body = {};


    new FormData(form)
        .forEach(
            (value, key) => {

                body[key] =
                    value;

            }
        );


    const result =
        await postData(
            endpoint,
            body
        );


    if (result) {

        alert(
            "Data saved successfully."
        );


        form.reset();

    }

}


/* =========================================================
   16. SUPPLIER DROPDOWN
   ========================================================= */

async function loadSupplierDropdown(
    selectId
) {

    const suppliers =
        await fetchData(
            "/suppliers/"
        );


    if (!suppliers) {

        return;

    }


    const select =
        document.getElementById(
            selectId
        );


    if (!select) {

        return;

    }


    select.innerHTML = `

        <option value="">
            Select Supplier
        </option>

    `;


    suppliers.forEach(
        supplier => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                supplier.supplier_id;


            option.textContent =
                supplier.supplier_name;


            select.appendChild(
                option
            );

        }
    );

}


/* =========================================================
   17. PRODUCT DROPDOWN
   ========================================================= */

async function loadProductDropdown(
    selectId
) {

    const products =
        await fetchData(
            "/products/"
        );


    if (!products) {

        return;

    }


    const select =
        document.getElementById(
            selectId
        );


    if (!select) {

        return;

    }


    select.innerHTML = `

        <option value="">
            Select Product
        </option>

    `;


    products.forEach(
        product => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                product.product_id;


            option.textContent =
                product.product_name;


            select.appendChild(
                option
            );

        }
    );

}


/* =========================================================
   18. LOAD PRODUCTS
   ========================================================= */

async function loadProducts() {

    const products =
        await fetchData(
            "/products/"
        );


    if (!products) {

        return;

    }


    /* Product ID 1 → 20 */

    products.sort(
        (a, b) =>
            Number(a.product_id) -
            Number(b.product_id)
    );


    const tbody =
        document.getElementById(
            "productsTable"
        );


    if (!tbody) {

        return;

    }


    tbody.innerHTML = "";


    products.forEach(
        product => {

            tbody.innerHTML += `

                <tr>

                    <td>
                        ${product.product_id}
                    </td>

                    <td>
                        ${product.product_name ?? "-"}
                    </td>

                    <td>
                        ${product.category ?? "-"}
                    </td>

                    <td>
                        ${product.unit_price ?? 0}
                    </td>

                    <td>
                        ${product.supplier_id ?? "-"}
                    </td>

                </tr>

            `;

        }
    );

}


/* =========================================================
   19. LOAD SUPPLIERS
   ========================================================= */

async function loadSuppliers() {

    const suppliers =
        await fetchData(
            "/suppliers/"
        );


    if (!suppliers) {

        return;

    }


    /* Supplier ID 1 → 20 */

    suppliers.sort(
        (a, b) =>
            Number(a.supplier_id) -
            Number(b.supplier_id)
    );


    const tbody =
        document.getElementById(
            "suppliersTable"
        );


    if (!tbody) {

        return;

    }


    tbody.innerHTML = "";


    suppliers.forEach(
        supplier => {

            tbody.innerHTML += `

                <tr>

                    <td>
                        ${supplier.supplier_id}
                    </td>

                    <td>
                        ${supplier.supplier_name ?? "-"}
                    </td>

                    <td>
                        ${supplier.contact_person ?? "-"}
                    </td>

                    <td>
                        ${supplier.email ?? "-"}
                    </td>

                    <td>
                        ${supplier.phone ?? "-"}
                    </td>

                    <td>
                        ${supplier.address ?? "-"}
                    </td>

                </tr>

            `;

        }
    );

}


/* =========================================================
   20. LOAD INVENTORY
   ========================================================= */

async function loadInventory() {

    const inventory =
        await fetchData(
            "/inventory/"
        );


    if (!inventory) {

        return;

    }


    /* Product ID 1 → 20 */

    inventory.sort(
        (a, b) =>
            Number(a.product_id) -
            Number(b.product_id)
    );


    const tbody =
        document.getElementById(
            "inventoryTable"
        );


    if (!tbody) {

        return;

    }


    tbody.innerHTML = "";


    inventory.forEach(
        item => {

            let status =
                "Normal";


            if (
                Number(item.quantity) <=
                Number(item.minimum_stock)
            ) {

                status =
                    "Low Stock";

            }


            tbody.innerHTML += `

                <tr>

                    <td>
                        ${item.inventory_id ?? "-"}
                    </td>

                    <td>
                        ${item.product_id ?? "-"}
                    </td>

                    <td>
                        ${item.product_name ?? "-"}
                    </td>

                    <td>
                        ${item.quantity ?? 0}
                    </td>

                    <td>
                        ${item.minimum_stock ?? 0}
                    </td>

                    <td>
                        ${status}
                    </td>

                    <td>
                        ${item.last_updated ?? "-"}
                    </td>

                </tr>

            `;

        }
    );

}


/* =========================================================
   21. LOAD LOW STOCK
   ========================================================= */

async function loadLowStock() {

    const data =
        await fetchData(
            "/inventory/low-stock"
        );


    if (!data) {

        return;

    }


    const tbody =
        document.getElementById(
            "lowStockBody"
        );


    if (!tbody) {

        return;

    }


    tbody.innerHTML = "";


    if (
        data.length === 0
    ) {

        tbody.innerHTML = `

            <tr>

                <td colspan="5">

                    No low-stock products.

                </td>

            </tr>

        `;

        return;

    }


    data.forEach(
        item => {

            tbody.innerHTML += `

                <tr>

                    <td>
                        ${item.product_id ?? "-"}
                    </td>

                    <td>
                        ${item.product_name ?? "-"}
                    </td>

                    <td>
                        ${item.quantity ?? 0}
                    </td>

                    <td>
                        ${item.minimum_stock ?? 0}
                    </td>

                    <td>
                        Low Stock
                    </td>

                </tr>

            `;

        }
    );

}


/* =========================================================
   22. LOAD SALES
   ========================================================= */

async function loadSales() {

    const sales =
        await fetchData(
            "/sales/"
        );


    if (!sales) {

        return;

    }


    /* =====================================================
       IMPORTANT:
       Sale ID 1 → 20
       ===================================================== */

    sales.sort(
        (a, b) =>
            Number(a.sale_id) -
            Number(b.sale_id)
    );


    const tbody =
        document.getElementById(
            "salesTable"
        );


    if (!tbody) {

        return;

    }


    tbody.innerHTML = "";


    if (
        sales.length === 0
    ) {

        tbody.innerHTML = `

            <tr>

                <td colspan="5">

                    No sales records found.

                </td>

            </tr>

        `;

        return;

    }


    sales.forEach(
        sale => {


            /*
             * Product ID
             *
             * Supports both:
             * product_id
             * productId
             */

            const productId =
                sale.product_id ??
                sale.productId ??
                "-";


            tbody.innerHTML += `

                <tr>

                    <td>
                        ${sale.sale_id ?? "-"}
                    </td>

                    <td>
                        ${productId}
                    </td>

                    <td>
                        ${sale.quantity ?? 0}
                    </td>

                    <td>
                        ${sale.selling_price ?? 0}
                    </td>

                    <td>
                        ${sale.sale_date ?? "-"}
                    </td>

                </tr>

            `;

        }
    );

}


/* =========================================================
   23. ADD SALE
   ========================================================= */

async function addSale() {

    const productElement =
        document.getElementById(
            "product_id"
        );


    const quantityElement =
        document.getElementById(
            "quantity"
        );


    const priceElement =
        document.getElementById(
            "selling_price"
        );


    const dateElement =
        document.getElementById(
            "sale_date"
        );


    if (
        !productElement ||
        !quantityElement ||
        !priceElement ||
        !dateElement
    ) {

        alert(
            "Sales form fields are missing."
        );

        return;

    }


    const productId =
        Number(
            productElement.value
        );


    const quantity =
        Number(
            quantityElement.value
        );


    const sellingPrice =
        Number(
            priceElement.value
        );


    const saleDate =
        dateElement.value;


    if (!productId) {

        alert(
            "Please select a product."
        );

        return;

    }


    if (quantity <= 0) {

        alert(
            "Quantity must be greater than 0."
        );

        return;

    }


    if (sellingPrice < 0) {

        alert(
            "Selling price cannot be negative."
        );

        return;

    }


    if (!saleDate) {

        alert(
            "Please select sale date."
        );

        return;

    }


    const saleData = {

        product_id:
            productId,

        quantity:
            quantity,

        selling_price:
            sellingPrice,

        sale_date:
            saleDate

    };


    const result =
        await postData(
            "/sales/",
            saleData
        );


    if (result) {

        alert(
            "Sale added successfully."
        );


        document.getElementById(
            "saleForm"
        )?.reset();


        await loadSales();


        /* Refresh inventory */

        if (
            document.getElementById(
                "inventoryTable"
            )
        ) {

            await loadInventory();

        }

    }

}


/* =========================================================
   24. UPDATE INVENTORY
   ========================================================= */

async function updateInventory(
    productId
) {

    const quantityElement =
        document.getElementById(
            "quantity"
        );


    const minimumElement =
        document.getElementById(
            "minimum_stock"
        );


    if (
        !quantityElement ||
        !minimumElement
    ) {

        alert(
            "Inventory fields are missing."
        );

        return;

    }


    const quantity =
        Number(
            quantityElement.value
        );


    const minimumStock =
        Number(
            minimumElement.value
        );


    if (quantity < 0) {

        alert(
            "Quantity cannot be negative."
        );

        return;

    }


    if (minimumStock < 0) {

        alert(
            "Minimum stock cannot be negative."
        );

        return;

    }


    const result =
        await putData(
            "/inventory/" +
            productId +
            "?quantity=" +
            quantity +
            "&minimum_stock=" +
            minimumStock,
            {}
        );


    if (result) {

        alert(
            "Inventory updated successfully."
        );


        await loadInventory();

        await loadLowStock();

    }

}


/* =========================================================
   25. SAVE PRODUCT
   ========================================================= */

async function saveProduct() {

    const productId =
        document.getElementById(
            "product_id"
        )?.value;


    const productName =
        document.getElementById(
            "product_name"
        )?.value;


    const category =
        document.getElementById(
            "category"
        )?.value;


    const unitPrice =
        Number(
            document.getElementById(
                "unit_price"
            )?.value
        );


    const supplierId =
        Number(
            document.getElementById(
                "supplier_id"
            )?.value
        );


    const body = {

        product_name:
            productName,

        category:
            category,

        unit_price:
            unitPrice,

        supplier_id:
            supplierId

    };


    let result;


    if (productId) {

        result =
            await putData(
                "/products/" +
                productId,
                body
            );

    } else {

        result =
            await postData(
                "/products/",
                body
            );

    }


    if (result) {

        alert(
            productId
                ? "Product updated successfully."
                : "Product added successfully."
        );


        document.getElementById(
            "productForm"
        )?.reset();


        const hiddenId =
            document.getElementById(
                "product_id"
            );


        if (hiddenId) {

            hiddenId.value =
                "";

        }


        await loadProducts();

    }

}


/* =========================================================
   26. DELETE PRODUCT
   ========================================================= */

async function deleteProduct(
    productId
) {

    const confirmation =
        confirm(
            "Are you sure you want to delete this product?"
        );


    if (!confirmation) {

        return;

    }


    const result =
        await deleteData(
            "/products/" +
            productId
        );


    if (result) {

        alert(
            "Product deleted successfully."
        );


        await loadProducts();

    }

}


/* =========================================================
   27. SAVE SUPPLIER
   ========================================================= */

async function saveSupplier() {

    const supplierId =
        document.getElementById(
            "supplier_id"
        )?.value;


    const body = {

        supplier_name:
            document.getElementById(
                "supplier_name"
            )?.value,

        contact_person:
            document.getElementById(
                "contact_person"
            )?.value,

        email:
            document.getElementById(
                "email"
            )?.value,

        phone:
            document.getElementById(
                "phone"
            )?.value,

        address:
            document.getElementById(
                "address"
            )?.value

    };


    let result;


    if (supplierId) {

        result =
            await putData(
                "/suppliers/" +
                supplierId,
                body
            );

    } else {

        result =
            await postData(
                "/suppliers/",
                body
            );

    }


    if (result) {

        alert(
            supplierId
                ? "Supplier updated successfully."
                : "Supplier added successfully."
        );


        document.getElementById(
            "supplierForm"
        )?.reset();


        const hiddenId =
            document.getElementById(
                "supplier_id"
            );


        if (hiddenId) {

            hiddenId.value =
                "";

        }


        await loadSuppliers();

    }

}


/* =========================================================
   28. DELETE SUPPLIER
   ========================================================= */

async function deleteSupplier(
    supplierId
) {

    const confirmation =
        confirm(
            "Are you sure you want to delete this supplier?"
        );


    if (!confirmation) {

        return;

    }


    const result =
        await deleteData(
            "/suppliers/" +
            supplierId
        );


    if (result) {

        alert(
            "Supplier deleted successfully."
        );


        await loadSuppliers();

    }

}


/* =========================================================
   29. LOAD REPORT PRODUCTS
   ========================================================= */

async function loadReportProducts() {

    const products =
        await fetchData(
            "/products/"
        );


    if (!products) {

        return;

    }


    const select =
        document.getElementById(
            "reportProduct"
        );


    if (!select) {

        return;

    }


    select.innerHTML = `

        <option value="">
            All Products
        </option>

    `;


    products.sort(
        (a, b) =>
            Number(a.product_id) -
            Number(b.product_id)
    );


    products.forEach(
        product => {

            select.innerHTML += `

                <option
                    value="${product.product_id}"
                >

                    ${product.product_name}

                </option>

            `;

        }
    );

}


/* =========================================================
   30. LOAD REPORT CATEGORIES
   ========================================================= */

async function loadReportCategories() {

    const products =
        await fetchData(
            "/products/"
        );


    if (!products) {

        return;

    }


    const categories =
        [
            ...new Set(

                products
                    .map(
                        product =>
                            product.category
                    )
                    .filter(Boolean)

            )
        ];


    const select =
        document.getElementById(
            "reportCategory"
        );


    if (!select) {

        return;

    }


    select.innerHTML = `

        <option value="">
            All Categories
        </option>

    `;


    categories.forEach(
        category => {

            select.innerHTML += `

                <option
                    value="${category}"
                >

                    ${category}

                </option>

            `;

        }
    );

}


/* =========================================================
   31. LOAD SALES REPORT
   ========================================================= */

async function loadSalesReport() {

    const fromDate =
        document.getElementById(
            "fromDate"
        )?.value;


    const toDate =
        document.getElementById(
            "toDate"
        )?.value;


    const productId =
        document.getElementById(
            "reportProduct"
        )?.value;


    const category =
        document.getElementById(
            "reportCategory"
        )?.value;


    const params =
        new URLSearchParams();


    if (fromDate) {

        params.append(
            "from_date",
            fromDate
        );

    }


    if (toDate) {

        params.append(
            "to_date",
            toDate
        );

    }


    if (productId) {

        params.append(
            "product_id",
            productId
        );

    }


    if (category) {

        params.append(
            "category",
            category
        );

    }


    let endpoint =
        "/reports/sales";


    if (params.toString()) {

        endpoint +=
            "?" +
            params.toString();

    }


    const data =
        await fetchData(
            endpoint
        );


    if (!data) {

        return;

    }


    window.currentSalesReport =
        data;


    const tbody =
        document.getElementById(
            "salesReportBody"
        );


    if (!tbody) {

        return;

    }


    tbody.innerHTML = "";


    let total =
        0;


    data.forEach(
        sale => {

            const amount =
                Number(
                    sale.quantity
                ) *
                Number(
                    sale.selling_price
                );


            total +=
                amount;


            tbody.innerHTML += `

                <tr>

                    <td>
                        ${sale.sale_id ?? "-"}
                    </td>

                    <td>
                        ${sale.product_name ?? "-"}
                    </td>

                    <td>
                        ${sale.category ?? "-"}
                    </td>

                    <td>
                        ${sale.quantity ?? 0}
                    </td>

                    <td>
                        ${sale.selling_price ?? 0}
                    </td>

                    <td>
                        ${amount.toFixed(2)}
                    </td>

                    <td>
                        ${sale.sale_date ?? "-"}
                    </td>

                </tr>

            `;

        }
    );


    const reportSales =
        document.getElementById(
            "reportSales"
        );


    if (reportSales) {

        reportSales.innerText =
            total.toFixed(2);

    }


    const reportTransactions =
        document.getElementById(
            "reportTransactions"
        );


    if (reportTransactions) {

        reportTransactions.innerText =
            data.length;

    }

}


/* =========================================================
   32. LOAD PURCHASE REPORT
   =========================================================

   NOTE:
   This is NOT purchase management.
   It is only needed if your reports.html displays
   purchase reports.

   ========================================================= */

async function loadPurchaseReport() {

    const fromDate =
        document.getElementById(
            "fromDate"
        )?.value;


    const toDate =
        document.getElementById(
            "toDate"
        )?.value;


    const productId =
        document.getElementById(
            "reportProduct"
        )?.value;


    const category =
        document.getElementById(
            "reportCategory"
        )?.value;


    const params =
        new URLSearchParams();


    if (fromDate) {

        params.append(
            "from_date",
            fromDate
        );

    }


    if (toDate) {

        params.append(
            "to_date",
            toDate
        );

    }


    if (productId) {

        params.append(
            "product_id",
            productId
        );

    }


    if (category) {

        params.append(
            "category",
            category
        );

    }


    let endpoint =
        "/reports/purchases";


    if (params.toString()) {

        endpoint +=
            "?" +
            params.toString();

    }


    const data =
        await fetchData(
            endpoint
        );


    if (!data) {

        return;

    }


    window.currentPurchaseReport =
        data;


    const tbody =
        document.getElementById(
            "purchaseReportBody"
        );


    if (!tbody) {

        return;

    }


    tbody.innerHTML = "";


    let total =
        0;


    data.forEach(
        purchase => {

            const amount =
                Number(
                    purchase.quantity
                ) *
                Number(
                    purchase.purchase_price
                );


            total +=
                amount;


            tbody.innerHTML += `

                <tr>

                    <td>
                        ${purchase.purchase_id ?? "-"}
                    </td>

                    <td>
                        ${purchase.product_name ?? "-"}
                    </td>

                    <td>
                        ${purchase.category ?? "-"}
                    </td>

                    <td>
                        ${purchase.quantity ?? 0}
                    </td>

                    <td>
                        ${purchase.purchase_price ?? 0}
                    </td>

                    <td>
                        ${amount.toFixed(2)}
                    </td>

                    <td>
                        ${purchase.purchase_date ?? "-"}
                    </td>

                </tr>

            `;

        }
    );


    const reportPurchases =
        document.getElementById(
            "reportPurchases"
        );


    if (reportPurchases) {

        reportPurchases.innerText =
            total.toFixed(2);

    }

}


/* =========================================================
   33. GENERATE REPORT
   ========================================================= */

async function generateReport() {

    await loadSalesReport();


    /*
     * Purchase report is included because
     * reports.html may contain purchase reporting.
     * It does NOT add purchase management functions.
     */

    await loadPurchaseReport();


    const sales =
        window.currentSalesReport ||
        [];


    const purchases =
        window.currentPurchaseReport ||
        [];


    let salesTotal =
        0;


    let purchaseTotal =
        0;


    sales.forEach(
        sale => {

            salesTotal +=

                Number(
                    sale.quantity
                ) *

                Number(
                    sale.selling_price
                );

        }
    );


    purchases.forEach(
        purchase => {

            purchaseTotal +=

                Number(
                    purchase.quantity
                ) *

                Number(
                    purchase.purchase_price
                );

        }
    );


    const profit =
        salesTotal -
        purchaseTotal;


    const reportSales =
        document.getElementById(
            "reportSales"
        );


    const reportPurchases =
        document.getElementById(
            "reportPurchases"
        );


    const reportProfit =
        document.getElementById(
            "reportProfit"
        );


    const reportTransactions =
        document.getElementById(
            "reportTransactions"
        );


    if (reportSales) {

        reportSales.innerText =
            salesTotal.toFixed(2);

    }


    if (reportPurchases) {

        reportPurchases.innerText =
            purchaseTotal.toFixed(2);

    }


    if (reportProfit) {

        reportProfit.innerText =
            profit.toFixed(2);

    }


    if (reportTransactions) {

        reportTransactions.innerText =
            sales.length +
            purchases.length;

    }

}


/* =========================================================
   34. CLEAR REPORT FILTERS
   ========================================================= */

function clearReportFilters() {

    const ids = [

        "fromDate",

        "toDate",

        "reportProduct",

        "reportCategory"

    ];


    ids.forEach(
        id => {

            const element =
                document.getElementById(
                    id
                );


            if (!element) {

                return;

            }


            if (
                element.tagName ===
                "SELECT"
            ) {

                element.selectedIndex =
                    0;

            } else {

                element.value =
                    "";

            }

        }
    );


    const salesBody =
        document.getElementById(
            "salesReportBody"
        );


    const purchaseBody =
        document.getElementById(
            "purchaseReportBody"
        );


    if (salesBody) {

        salesBody.innerHTML =
            "";

    }


    if (purchaseBody) {

        purchaseBody.innerHTML =
            "";

    }


    [
        "reportSales",
        "reportPurchases",
        "reportProfit",
        "reportTransactions"
    ]
    .forEach(
        id => {

            const element =
                document.getElementById(
                    id
                );


            if (element) {

                element.innerText =
                    "0";

            }

        }
    );

}


/* =========================================================
   35. CSV EXPORT
   ========================================================= */

function downloadCSV(
    data,
    filename
) {

    if (
        !data ||
        data.length === 0
    ) {

        alert(
            "No data available for CSV export."
        );

        return;

    }


    const headers =
        Object.keys(
            data[0]
        );


    let csv =
        headers.join(",") +
        "\n";


    data.forEach(
        row => {

            const values =
                headers.map(
                    header => {

                        let value =
                            row[header] ??
                            "";


                        value =
                            String(value)
                            .replace(
                                /"/g,
                                '""'
                            );


                        return (
                            '"' +
                            value +
                            '"'
                        );

                    }
                );


            csv +=
                values.join(",") +
                "\n";

        }
    );


    const blob =
        new Blob(
            [csv],
            {
                type:
                    "text/csv;charset=utf-8;"
            }
        );


    const url =
        URL.createObjectURL(
            blob
        );


    const link =
        document.createElement(
            "a"
        );


    link.href =
        url;


    link.download =
        filename;


    document.body.appendChild(
        link
    );


    link.click();


    document.body.removeChild(
        link
    );


    URL.revokeObjectURL(
        url
    );

}


/* =========================================================
   36. EXPORT SALES CSV
   ========================================================= */

function exportSalesCSV() {

    downloadCSV(

        window.currentSalesReport ||
        [],

        "sales_report.csv"

    );

}


/* =========================================================
   37. EXPORT PURCHASE CSV
   =========================================================

   Only for Reports page.
   ========================================================= */

function exportPurchaseCSV() {

    downloadCSV(

        window.currentPurchaseReport ||
        [],

        "purchase_report.csv"

    );

}


/* =========================================================
   38. LOAD PROFILE
   ========================================================= */

async function loadProfile() {

    const user =
        await checkLogin();


    if (!user) {

        return;

    }


    const username =
        user.username ||
        "-";


    const role =
        user.role ||
        "User";


    const fullName =
        user.full_name ||
        username;


    const email =
        user.Email ||
        user.email ||
        "-";


    const userId =
        user.user_id ||
        "-";


    const elements = {

        displayName:
            fullName,

        displayEmail:
            email,

        displayRole:
            role,

        fullName:
            fullName,

        username:
            username,

        email:
            email,

        role:
            role,

        userId:
            userId

    };


    Object.keys(elements)
        .forEach(
            id => {

                const element =
                    document.getElementById(
                        id
                    );


                if (element) {

                    element.innerText =
                        elements[id];

                }

            }
        );

}


/* =========================================================
   39. INDEX PROFILE ICON
   ========================================================= */

async function updateIndexProfile() {

    const token =
        getToken();


    const loginLink =
        document.getElementById(
            "loginLink"
        );


    const registerLink =
        document.getElementById(
            "registerLink"
        );


    const profileIcon =
        document.getElementById(
            "profileIcon"
        );


    const authButtons =
        document.getElementById(
            "authButtons"
        );


    /* ==============================================
       USER NOT LOGGED IN
       ============================================== */

    if (!token) {


        if (loginLink) {

            loginLink.style.display =
                "";

        }


        if (registerLink) {

            registerLink.style.display =
                "";

        }


        if (profileIcon) {

            profileIcon.style.display =
                "none";

        }


        if (authButtons) {

            authButtons.style.display =
                "flex";

        }


        return;

    }


    /* ==============================================
       CHECK TOKEN
       ============================================== */

    const user =
        await getCurrentUser();


    if (!user) {

        removeToken();


        if (loginLink) {

            loginLink.style.display =
                "";

        }


        if (registerLink) {

            registerLink.style.display =
                "";

        }


        if (profileIcon) {

            profileIcon.style.display =
                "none";

        }


        if (authButtons) {

            authButtons.style.display =
                "flex";

        }


        return;

    }


    /* ==============================================
       USER LOGGED IN
       ============================================== */

    if (loginLink) {

        loginLink.style.display =
            "none";

    }


    if (registerLink) {

        registerLink.style.display =
            "none";

    }


    if (profileIcon) {

        profileIcon.style.display =
            "flex";

    }


    if (authButtons) {

        authButtons.style.display =
            "none";

    }

}


/* =========================================================
   40. PAGE INITIALIZATION
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    async function () {


        /* ==============================================
           INDEX PAGE
           ============================================== */

        if (
            document.getElementById(
                "profileIcon"
            )
        ) {

            await updateIndexProfile();

        }


        /* ==============================================
           DASHBOARD
           ============================================== */

        if (
            document.getElementById(
                "totalProducts"
            )
        ) {

            const user =
                await checkLogin();


            if (user) {

                applyRoleBasedUI(
                    user
                );


                await loadDashboard();

            }

        }


        /* ==============================================
           PRODUCTS
           ============================================== */

        if (
            document.getElementById(
                "productsTable"
            )
        ) {

            const user =
                await checkLogin();


            if (user) {

                applyRoleBasedUI(
                    user
                );


                await loadProducts();


                await loadSupplierDropdown(
                    "supplier_id"
                );

            }

        }


        /* ==============================================
           SUPPLIERS
           ============================================== */

        if (
            document.getElementById(
                "suppliersTable"
            )
        ) {

            const user =
                await checkLogin();


            if (user) {

                applyRoleBasedUI(
                    user
                );


                await loadSuppliers();

            }

        }


        /* ==============================================
           INVENTORY
           ============================================== */

        if (
            document.getElementById(
                "inventoryTable"
            )
        ) {

            const user =
                await checkLogin();


            if (user) {

                applyRoleBasedUI(
                    user
                );


                await loadInventory();


                await loadLowStock();

            }

        }


        /* ==============================================
           SALES
           ============================================== */

        if (
            document.getElementById(
                "salesTable"
            )
        ) {

            const user =
                await checkLogin();


            if (user) {

                applyRoleBasedUI(
                    user
                );


                await loadProductDropdown(
                    "product_id"
                );


                await loadSales();

            }

        }


        /* ==============================================
           PROFILE
           ============================================== */

        if (
            document.getElementById(
                "profileContent"
            )
        ) {

            await loadProfile();

        }


        /* ==============================================
           REPORTS
           ============================================== */

        if (
            document.getElementById(
                "salesReportBody"
            )
        ) {

            const user =
                await checkLogin();


            if (user) {

                applyRoleBasedUI(
                    user
                );


                await loadReportProducts();


                await loadReportCategories();

            }

        }

    }
);


/* =========================================================
   END OF JAVASCRIPT FILE
   ========================================================= */