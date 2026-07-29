// ======================================
// API URL
// ======================================

const BASE_URL = "http://127.0.0.1:8000";


// ======================================
// JWT TOKEN
// ======================================

function getToken() {

    return localStorage.getItem("access_token");

}

function saveToken(token) {

    localStorage.setItem("access_token", token);

}

function logout() {

    localStorage.removeItem("access_token");

    window.location.href = "index.html";

}


// ======================================
// LOGIN
// ======================================

async function login(username, password) {

    const formData = new URLSearchParams();

    formData.append("username", username);

    formData.append("password", password);

    const response = await fetch(BASE_URL + "/auth/login", {

        method: "POST",

        headers: {

            "Content-Type": "application/x-www-form-urlencoded"

        },

        body: formData

    });

    const data = await response.json();

    if (response.ok) {

        saveToken(data.access_token);

        window.location.href = "dashboard.html";

    }

    else {

        alert(data.detail);

    }

}


// ======================================
// FETCH GET
// ======================================

async function fetchData(endpoint) {

    const response = await fetch(BASE_URL + endpoint, {

        headers: {

            "Authorization": "Bearer " + getToken()

        }

    });

    return await response.json();

}


// ======================================
// FETCH POST
// ======================================

async function postData(endpoint, body) {

    const response = await fetch(BASE_URL + endpoint, {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

            "Authorization": "Bearer " + getToken()

        },

        body: JSON.stringify(body)

    });

    return await response.json();

}


// ======================================
// FETCH PUT
// ======================================

async function putData(endpoint, body) {

    const response = await fetch(BASE_URL + endpoint, {

        method: "PUT",

        headers: {

            "Content-Type": "application/json",

            "Authorization": "Bearer " + getToken()

        },

        body: JSON.stringify(body)

    });

    return await response.json();

}


// ======================================
// FETCH DELETE
// ======================================

async function deleteData(endpoint) {

    const response = await fetch(BASE_URL + endpoint, {

        method: "DELETE",

        headers: {

            "Authorization": "Bearer " + getToken()

        }

    });

    return await response.json();

}


// ======================================
// LOAD TABLE
// ======================================

function loadTable(data, tbodyId, columns) {

    const tbody = document.getElementById(tbodyId);

    tbody.innerHTML = "";

    data.forEach(item => {

        let row = "<tr>";

        columns.forEach(column => {

            row += `<td>${item[column]}</td>`;

        });

        row += "</tr>";

        tbody.innerHTML += row;

    });

}


// ======================================
// FORM SUBMIT
// ======================================

async function submitForm(formId, endpoint) {

    const form = document.getElementById(formId);

    const body = {};

    new FormData(form).forEach((value, key) => {

        body[key] = value;

    });

    await postData(endpoint, body);

    form.reset();

}


// ======================================
// DASHBOARD
// ======================================

async function loadDashboard() {

    const data = await fetchData("/reports/dashboard");

    document.getElementById("totalProducts").innerText =
        data.total_products;

    document.getElementById("totalSuppliers").innerText =
        data.total_suppliers;

    document.getElementById("totalSales").innerText =
        data.total_sales_amount;

    document.getElementById("totalPurchases").innerText =
        data.total_purchase_amount;

    document.getElementById("lowStock").innerText =
        data.low_stock_products;

}