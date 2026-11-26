from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.automation.employee import add_employee
from app.automation.extractor import extract_employee_list

def run_automation(username, password, first_name, last_name, employee_id):
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://opensource-demo.orangehrmlive.com")

        wait.until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys(username)

        driver.find_element(By.NAME, "password").send_keys(password)

        driver.find_element(
            By.CSS_SELECTOR, "button[type='submit']"
        ).click()

        try:
            wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//h6[text()='Dashboard']")
                )
            )
            print("Login successful!")

        except Exception:
            driver.save_screenshot("screenshots/login_error.png")
            raise Exception(
                "OrangeHRM login failed. Please check username and password."
            )

        print("Login successful!")

        add_employee(
            driver,
            first_name,
            last_name,
            employee_id
        )

        print("Employee created successfully!")

        # Extract employee list
        employees = extract_employee_list(driver)

        return {
            "status": "success",
            "message": "Employee created and list extracted successfully!",
            "employee": {
                "first_name": first_name,
                "last_name": last_name,
                "employee_id": employee_id
            },
            "employees": employees
        }


    except Exception as e:

        import traceback

        print("Automation failed!")

        print("Error type:", type(e).__name__)

        print("Error details:", repr(e))

        traceback.print_exc()

        driver.save_screenshot("screenshots/automation_error.png")

        return {

            "status": "failed",

            "error_type": type(e).__name__,

            "message": repr(e)

        }

    finally:
        driver.quit()