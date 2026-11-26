
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.automation.employee import add_employee
from app.automation.extractor import extract_employee_list
from app.automation.logger import logger


def run_automation(username, password, first_name, last_name, employee_id):

    driver = None

    logger.info("========== AUTOMATION STARTED ==========")

    try:
        # Create required directories
        os.makedirs("screenshots", exist_ok=True)
        os.makedirs("exports", exist_ok=True)

        # Step 1: Configure Chrome
        logger.info("Step 1: Configuring Chrome browser")

        options = Options()
        options.add_argument("--start-maximized")

        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 30)

        logger.info("Chrome browser started successfully")

        # Step 2: Open OrangeHRM
        logger.info("Step 2: Opening OrangeHRM website")

        driver.get("https://opensource-demo.orangehrmlive.com")

        # Step 3: Enter username
        logger.info("Step 3: Entering username")

        username_field = wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "username")
            )
        )
        username_field.send_keys(username)

        # Step 4: Enter password
        logger.info("Step 4: Entering password")

        password_field = driver.find_element(
            By.NAME, "password"
        )
        password_field.send_keys(password)

        # Step 5: Login
        logger.info("Step 5: Submitting login form")

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

        logger.info("Login successful")

        # Screenshot 1: Before employee creation
        logger.info("Capturing before execution screenshot")

        driver.save_screenshot(
            "screenshots/before_execution.png"
        )

        logger.info("Before execution screenshot saved")

        # Step 6: Create and verify employee
        logger.info(
            "Step 6: Creating employee with ID: %s",
            employee_id
        )

        add_employee(
            driver,
            first_name,
            last_name,
            employee_id
        )

        logger.info("Employee created and verified successfully")

        # Step 7: Extract employee list
        logger.info("Step 7: Starting employee list extraction")

        employees = extract_employee_list(driver)

        logger.info(
            "Employee list extraction completed. Total records: %s",
            len(employees)
        )

        # Screenshot 2: After employee creation and extraction
        logger.info("Capturing after execution screenshot")

        driver.save_screenshot(
            "screenshots/after_execution.png"
        )

        logger.info("After execution screenshot saved")

        # Step 8: Logout from OrangeHRM
        logger.info("Step 8: Opening user profile menu")

        wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".oxd-userdropdown-tab")
            )
        ).click()

        logger.info("Clicking logout")

        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[normalize-space()='Logout']")
            )
        ).click()

        # Step 9: Verify logout
        logger.info("Step 9: Verifying logout")

        wait.until(
            EC.visibility_of_element_located(
                (By.NAME, "username")
            )
        )

        logger.info("Logout successful")

        logger.info("========== AUTOMATION COMPLETED ==========")

        return {
            "status": "success",
            "message": (
                "Employee created, verified, extracted "
                "and logged out successfully!"
            ),
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

        logger.error("Automation failed")
        logger.error("Error type: %s", type(e).__name__)
        logger.exception("Automation exception details")

        if driver:
            try:
                driver.save_screenshot(
                    "screenshots/automation_error.png"
                )
                logger.info("Error screenshot saved")
            except Exception:
                logger.exception("Could not save error screenshot")

        return {
            "status": "failed",
            "error_type": type(e).__name__,
            "message": str(e)
        }

    finally:

        if driver:
            driver.quit()
            logger.info("Chrome browser closed")

