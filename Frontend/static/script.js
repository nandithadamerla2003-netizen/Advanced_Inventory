// API URL

const BASE_URL = "http://127.0.0.1:8000";

// JWT TOKEN

function getToken() {

    return localStorage.getItem("access_token");

}

function saveToken(token) {

    localStorage.setItem("access_token", token);

}

function logout() {

    localStorage.removeItem("access_token");

    alert("Logged out successfully.");

    window.location.href = "login.html";

}

// CHECK LOGIN

function checkLogin() {

    const token = getToken();

    if (!token) {

        alert("Please login first.");

        window.location.href = "login.html";

    }

}

// LOGIN

async function login(Email, username, password) {

    try {

        const response = await fetch(BASE_URL + "/auth/login", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                Email: Email,

                username: username,

                password: password

            })

        });

        const data = await response.json();

        if (response.ok) {

            saveToken(data.access_token);

            alert("Login Successful.");

            window.location.href = "dashboard.html";

        }

        else {

            alert(data.detail);

        }

    }

    catch (error) {

        alert("Unable to connect to server.");

        console.error(error);

    }

}

// REGISTER

async function register(full_name, Email, username, password) {

    try {

        const response = await fetch(BASE_URL + "/auth/register", {

            method: "POST",

            headers: {

                "Content-Type": "application/json"

            },

            body: JSON.stringify({

                full_name: full_name,

                Email: Email,

                username: username,

                password: password

            })

        });

        const data = await response.json();

        if (response.ok) {

            alert("Registration Successful.");

            window.location.href = "login.html";

        }

        else {

            alert(data.detail);

        }

    }

    catch (error) {

        alert("Unable to connect to server.");

        console.error(error);

    }

}

// FETCH GET

async function fetchData(endpoint) {

    try {

        const response = await fetch(BASE_URL + endpoint, {

            headers: {

                "Authorization": "Bearer " + getToken()

            }

        });

        if (response.status === 401) {

            alert("Session Expired. Please Login Again.");

            logout();

            return;

        }

        return await response.json();

    }

    catch (error) {

        console.error(error);

    }

}

// FETCH POST

async function postData(endpoint, body) {

    try {

        const response = await fetch(BASE_URL + endpoint, {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

                "Authorization": "Bearer " + getToken()

            },

            body: JSON.stringify(body)

        });

        const data = await response.json();

        if (!response.ok) {

            alert(data.detail);

            return null;

        }

        return data;

    }

    catch (error) {

        console.error(error);

    }

}

// FETCH PUT

async function putData(endpoint, body) {

    try {

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

    catch (error) {

        console.error(error);

    }

}

// FETCH DELETE

async function deleteData(endpoint) {

    try {

        const response = await fetch(BASE_URL + endpoint, {

            method: "DELETE",

            headers: {

                "Authorization": "Bearer " + getToken()

            }

        });

        return await response.json();

    }

    catch (error) {

        console.error(error);

    }

}

// LOAD TABLE

function loadTable(data, tbodyId, columns) {

    const tbody = document.getElementById(tbodyId);

    if (!tbody) return;

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

// FORM SUBMIT

async function submitForm(formId, endpoint) {

    const form = document.getElementById(formId);

    const body = {};

    new FormData(form).forEach((value, key) => {

        body[key] = value;

    });

    const result = await postData(endpoint, body);

    if (result) {

        alert("Data Saved Successfully.");

        form.reset();

    }

}

// DASHBOARD

async function loadDashboard() {

    const data = await fetchData("/reports/dashboard");

    if (!data) return;

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

// PAGE LOADER

document.addEventListener("DOMContentLoaded", () => {

    const page = window.location.pathname;

    if (page.includes("dashboard.html")) {

        checkLogin();

        loadDashboard();

    }

});