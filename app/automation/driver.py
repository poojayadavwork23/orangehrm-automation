
import os
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.automation.employee import add_employee
from app.automation.extractor import extract_employee_list


def run_automation(username, password, first_name, last_name, employee_id):

    driver = None

    try:
        os.makedirs("screenshots", exist_ok=True)
        os.makedirs("exports", exist_ok=True)

        # Step 1: Configure Chrome
        options = Options()
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=options)

        wait = WebDriverWait(driver, 30)

        # Step 2: Open OrangeHRM
        driver.get(
            "https://opensource-demo.orangehrmlive.com"
        )

        # Step 3: Enter username
        username_field = wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "username")
            )
        )

        username_field.send_keys(username)

        # Step 4: Enter password
        password_field = driver.find_element(
            By.NAME, "password"
        )

        password_field.send_keys(password)

        # Step 5: Login
        login_button = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[type='submit']")
            )
        )

        login_button.click()

        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h6[normalize-space()='Dashboard']")
            )
        )

        print("Login successful!")

        # Step 6: Create and verify employee
        add_employee(
            driver,
            first_name,
            last_name,
            employee_id
        )

        print("Employee created and verified successfully!")

        # Step 7: Extract employee list
        employees = extract_employee_list(driver)

        print("Employee list extracted successfully!")

        return {
            "status": "success",
            "message": "Employee created, verified and extracted successfully!",
            "employee": {
                "first_name": first_name,
                "last_name": last_name,
                "employee_id": employee_id
            },
            "total_employees": len(employees),
            "employees": employees,
            "csv_file": "exports/employees.csv"
        }

    except Exception as e:

        print("--------------------------------")
        print("Automation failed!")
        print("Error type:", type(e).__name__)
        print("Error details:", repr(e))
        traceback.print_exc()
        print("--------------------------------")

        if driver:
            driver.save_screenshot(
                "screenshots/automation_error.png"
            )

        return {
            "status": "failed",
            "error_type": type(e).__name__,
            "message": str(e)
        }

    finally:

        if driver:
            driver.quit()
