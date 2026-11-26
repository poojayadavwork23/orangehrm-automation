
import csv
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_employee_list(driver):
    wait = WebDriverWait(driver, 20)

    # Open PIM
    pim_menu = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='PIM']")
        )
    )
    pim_menu.click()

    # Open Employee List
    employee_list = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[text()='Employee List']")
        )
    )
    employee_list.click()

    # Wait for employee table
    wait.until(
        EC.visibility_of_element_located(
            (By.CLASS_NAME, "oxd-table-body")
        )
    )

    # Extract table headers
    headers = [
        cell.text.strip()
        for cell in driver.find_elements(
            By.CSS_SELECTOR, ".oxd-table-header .oxd-table-cell"
        )
    ]

    # Extract employee rows
    rows = driver.find_elements(
        By.CSS_SELECTOR, ".oxd-table-body .oxd-table-row"
    )

    employees = []

    for row in rows:
        cells = row.find_elements(
            By.CSS_SELECTOR, ".oxd-table-cell"
        )

        values = [cell.text.strip() for cell in cells]

        if values:
            employees.append(dict(zip(headers, values)))

    # Save CSV
    os.makedirs("exports", exist_ok=True)

    if employees:
        with open(
            "exports/employees.csv",
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

    print(f"Extracted {len(employees)} employees.")

    return employees
