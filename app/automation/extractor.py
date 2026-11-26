
import csv
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_loader(driver):
    WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located(
            (By.CLASS_NAME, "oxd-form-loader")
        )
    )


def get_employee_rows(driver):
    """
    Get employee table data using JavaScript.
    """

    return driver.execute_script("""
        const rows = document.querySelectorAll(
            '.oxd-table-body .oxd-table-row'
        );

        return Array.from(rows).map(row =>
            Array.from(
                row.querySelectorAll('.oxd-table-cell')
            ).map(cell => cell.innerText.trim())
        );
    """)


def extract_employee_list(driver):

    wait = WebDriverWait(driver, 30)

    headers = [
        "Employee ID",
        "First Name",
        "Last Name",
        "Job Title",
        "Employment Status",
        "Sub Unit"
    ]

    employees = []
    seen_employee_ids = set()

    # Step 1: Navigate to Employee List if needed
    if not driver.current_url.endswith("/pim/viewEmployeeList"):

        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='PIM']")
            )
        ).click()

        wait_for_loader(driver)

        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[normalize-space()='Employee List']")
            )
        ).click()

        wait_for_loader(driver)

    # Step 2: Wait for table
    wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".oxd-table-body")
        )
    )

    # Step 3: Reset previous filters
    reset_buttons = driver.find_elements(
        By.XPATH,
        "//button[.//span[normalize-space()='Reset']]"
    )

    if reset_buttons:
        reset_buttons[0].click()
        wait_for_loader(driver)

    # Step 4: Extract all pages
    while True:

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".oxd-table-body")
            )
        )

        rows = get_employee_rows(driver)

        print("Current page employee rows:", len(rows))

        for values in rows:

            if len(values) < 7 or not values[1].strip():
                continue

            employee = {
                "Employee ID": values[1].strip(),
                "First Name": values[2].strip(),
                "Last Name": values[3].strip(),
                "Job Title": values[4].strip(),
                "Employment Status": values[5].strip(),
                "Sub Unit": values[6].strip()
            }

            employee_id = employee["Employee ID"]

            if employee_id not in seen_employee_ids:
                employees.append(employee)
                seen_employee_ids.add(employee_id)

        # Step 5: Check Next Page
        next_buttons = driver.find_elements(
            By.CSS_SELECTOR,
            "button.oxd-pagination-page-item--next"
        )

        if not next_buttons:
            break

        next_button = next_buttons[0]

        button_class = next_button.get_attribute("class") or ""

        if (
            next_button.get_attribute("disabled") is not None
            or "oxd-pagination-page-item--disabled" in button_class
        ):
            break

        previous_first_row = rows[0] if rows else None

        next_button.click()

        # Step 6: Wait for next page
        def page_changed(driver):

            new_rows = get_employee_rows(driver)

            return (
                bool(new_rows)
                and new_rows[0] != previous_first_row
            )

        wait.until(page_changed)

    # Step 7: Save CSV
    os.makedirs("exports", exist_ok=True)

    csv_path = os.path.join(
        "exports",
        "employees.csv"
    )

    with open(
        csv_path,
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=headers
        )

        writer.writeheader()
        writer.writerows(employees)

    print("--------------------------------")
    print("Employee extraction completed!")
    print("Total employees:", len(employees))
    print("CSV saved:", csv_path)
    print("--------------------------------")

    return employees
