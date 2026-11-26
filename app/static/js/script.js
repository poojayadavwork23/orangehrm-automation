
const form = document.getElementById("employeeForm");
const resultDiv = document.getElementById("result");
const submitBtn = document.getElementById("submitBtn");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    submitBtn.disabled = true;
    submitBtn.innerHTML = "Automation Running...";

    resultDiv.style.display = "block";
    resultDiv.className = "alert alert-info mt-4";
    resultDiv.innerHTML = "Please wait. Employee automation is running...";

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
            throw new Error(data.message || "Employee automation failed.");
        }

        const employee = data.employee;

        resultDiv.className = "alert alert-success mt-4";
        resultDiv.innerHTML = `
            <h5><i class="bi bi-check-circle-fill me-2"></i>
                Employee Created Successfully!
            </h5>
            <hr>
            <p><strong>First Name:</strong> ${employee.first_name}</p>
            <p><strong>Last Name:</strong> ${employee.last_name}</p>
            <p><strong>Employee ID:</strong> ${employee.employee_id}</p>
            <strong>Status:</strong> Completed
        `;

    } catch (error) {
        resultDiv.className = "alert alert-danger mt-4";
        resultDiv.innerText = error.message;

    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML =
            '<i class="bi bi-play-circle-fill me-2"></i> Start Automation';
    }
});
