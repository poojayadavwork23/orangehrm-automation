
const form = document.getElementById("employeeForm");
const resultDiv = document.getElementById("result");
const submitBtn = document.getElementById("submitBtn");

function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;"
    })[char]);
}

function downloadCSV(employees) {
    if (!employees.length) return;

    const headers = Object.keys(employees[0]);

    const csvRows = [
        headers.join(","),
        ...employees.map(employee =>
            headers.map(header =>
                `"${String(employee[header] ?? "").replace(/"/g, '""')}"`
            ).join(",")
        )
    ];

    const blob = new Blob(
        [csvRows.join("\n")],
        { type: "text/csv;charset=utf-8;" }
    );

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = "employees.csv";
    link.click();

    URL.revokeObjectURL(url);
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    submitBtn.disabled = true;
    submitBtn.innerHTML = "Automation Running...";

    resultDiv.className = "alert alert-info mt-4";
    resultDiv.innerHTML = "Please wait. Automation is running...";

    const employeeData = {
        username: document.getElementById("username").value,
        password: document.getElementById("password").value,
        first_name: document.getElementById("first_name").value,
        last_name: document.getElementById("last_name").value,
        employee_id: document.getElementById("employee_id").value
    };

    try {
        const response = await fetch("/api/automation/start", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(employeeData)
        });

        const data = await response.json();

        if (!response.ok || data.status !== "success") {
            throw new Error(
                data.detail || data.message || "Automation failed."
            );
        }

        const employee = data.employee;
        const employees = data.employees || [];

        let tableHTML = "";

        if (employees.length) {
            const headers = Object.keys(employees[0]);

            tableHTML = `
                <h5 class="mt-4">Extracted Employee List</h5>
                <p>Total Employees: <strong>${employees.length}</strong></p>

                <div class="table-responsive">
                    <table class="table table-bordered table-striped">
                        <thead>
                            <tr>
                                ${headers.map(header =>
                                    `<th>${escapeHTML(header)}</th>`
                                ).join("")}
                            </tr>
                        </thead>
                        <tbody>
                            ${employees.map(emp => `
                                <tr>
                                    ${headers.map(header =>
                                        `<td>${escapeHTML(emp[header])}</td>`
                                    ).join("")}
                                </tr>
                            `).join("")}
                        </tbody>
                    </table>
                </div>

                <button type="button" id="downloadCsvBtn"
                        class="btn btn-success mt-2">
                    Download CSV
                </button>
            `;
        }

        resultDiv.className = "alert alert-success mt-4";

        resultDiv.innerHTML = `
            <h5>Employee Created Successfully!</h5>
            <hr>
            <p><strong>First Name:</strong> ${escapeHTML(employee.first_name)}</p>
            <p><strong>Last Name:</strong> ${escapeHTML(employee.last_name)}</p>
            <p><strong>Employee ID:</strong> ${escapeHTML(employee.employee_id)}</p>
            <p><strong>Status:</strong> Completed</p>
            ${tableHTML}
        `;

        const downloadBtn = document.getElementById("downloadCsvBtn");

        if (downloadBtn) {
            downloadBtn.addEventListener("click", () => {
                downloadCSV(employees);
            });
        }

    } catch (error) {
        resultDiv.className = "alert alert-danger mt-4";
        resultDiv.textContent = error.message;

    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML =
            '<i class="bi bi-play-circle-fill me-2"></i> Start Automation';
    }
});
