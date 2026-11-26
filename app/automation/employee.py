
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_for_loader(driver):
    """
    Wait until OrangeHRM form loader disappears.
    """
    WebDriverWait(driver, 30).until(
        EC.invisibility_of_element_located(
            (By.CSS_SELECTOR, ".oxd-form-loader")
        )
    )


def clear_and_type(field, value):
    """
    Clear existing input and enter new value.
    """
    field.click()
    field.send_keys(Keys.CONTROL, "a")
    field.send_keys(Keys.BACKSPACE)
    field.send_keys(str(value))


def get_table_rows(driver):
    """
    Read table data using JavaScript to avoid stale elements.
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


def add_employee(driver, first_name, last_name, employee_id):

    wait = WebDriverWait(driver, 30)

    try:

        # Step 1: Open PIM
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='PIM']")
            )
        ).click()

        wait_for_loader(driver)

        # Step 2: Open Add Employee
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[normalize-space()='Add Employee']")
            )
        ).click()

        # Wait for Add Employee page
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h6[normalize-space()='Add Employee']")
            )
        )

        wait_for_loader(driver)

        # Step 3: Enter First Name
        first_name_field = wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "firstName")
            )
        )

        clear_and_type(first_name_field, first_name)

        # Step 4: Enter Last Name
        last_name_field = wait.until(
            EC.element_to_be_clickable(
                (By.NAME, "lastName")
            )
        )

        clear_and_type(last_name_field, last_name)

        # Step 5: Enter Employee ID
        employee_id_field = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[normalize-space()='Employee Id']/following::input[1]"
                )
            )
        )

        clear_and_type(employee_id_field, employee_id)

        # Step 6: Validate input values
        actual_first = first_name_field.get_attribute("value").strip()
        actual_last = last_name_field.get_attribute("value").strip()
        actual_id = employee_id_field.get_attribute("value").strip()

        print("First Name:", actual_first)
        print("Last Name:", actual_last)
        print("Employee ID:", actual_id)

        if actual_first.lower() != first_name.strip().lower():
            raise Exception("First Name validation failed.")

        if actual_last.lower() != last_name.strip().lower():
            raise Exception("Last Name validation failed.")

        if actual_id != str(employee_id).strip():
            raise Exception("Employee ID validation failed.")

        # Step 7: Save Employee
        save_button = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[@type='submit' and contains(@class, 'oxd-button--secondary')]"
                )
            )
        )

        save_button.click()

        # Step 8: Verify successful employee creation

        # Wait until Personal Details URL opens
        wait.until(
            lambda d: "/pim/viewPersonalDetails/" in d.current_url
        )

        # Wait until Personal Details heading appears
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h6[normalize-space()='Personal Details']")
            )
        )

        print("Personal Details page opened.")

        # Wait for loading spinner to disappear
        wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".oxd-loading-spinner-container")
            )
        )

        # Find saved Employee ID using JavaScript
        saved_id = wait.until(
            lambda d: d.execute_script("""
                const groups = document.querySelectorAll(
                    '.oxd-input-group'
                );

                for (const group of groups) {
                    const label = group.querySelector('label');

                    if (
                        label &&
                        label.innerText.trim() === 'Employee Id'
                    ) {
                        const input = group.querySelector('input');

                        if (input && input.value.trim()) {
                            return input.value.trim();
                        }
                    }
                }

                return false;
            """)
        )

        print("Submitted Employee ID:", employee_id)
        print("Saved Employee ID:", saved_id)

        if saved_id != str(employee_id).strip():
            raise Exception(
                f"Employee ID mismatch. Expected {employee_id}, got {saved_id}"
            )

        print("Employee created and saved successfully!")

        # Step 9: Open Employee List
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[normalize-space()='Employee List']")
            )
        ).click()

        wait_for_loader(driver)

        wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".oxd-table-body")
            )
        )

        # Step 10: Search Employee ID
        search_id = wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//label[normalize-space()='Employee Id']/following::input[1]"
                )
            )
        )

        clear_and_type(search_id, employee_id)

        actual_search_id = search_id.get_attribute("value").strip()

        print("Search Employee ID:", actual_search_id)

        if actual_search_id != str(employee_id).strip():
            raise Exception("Search Employee ID validation failed.")

        # Capture current table before searching
        previous_table = driver.execute_script("""
            const table = document.querySelector('.oxd-table-body');
            return table ? table.innerText : '';
        """)

        # Step 11: Click Search
        search_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space()='Search']")
            )
        )

        search_button.click()

        # Wait for search results to update
        wait.until(
            lambda d: d.execute_script("""
                const table = document.querySelector('.oxd-table-body');
                return table && table.innerText !== arguments[0];
            """, previous_table)
        )

        # Step 12: Verify Employee ID and name
        def verify_employee(driver):

            rows = get_table_rows(driver)

            for values in rows:

                if len(values) >= 4:

                    actual_id = values[1].strip()
                    actual_first = values[2].strip()
                    actual_last = values[3].strip()

                    if (
                        actual_id == str(employee_id).strip()
                        and actual_first.lower() == first_name.strip().lower()
                        and actual_last.lower() == last_name.strip().lower()
                    ):
                        return values

            return False

        verified_employee = wait.until(verify_employee)

        print("--------------------------------")
        print("Employee verified successfully!")
        print("Verified employee:", verified_employee)
        print("--------------------------------")

        return True

    except Exception as e:

        os.makedirs("screenshots", exist_ok=True)

        driver.save_screenshot(
            "screenshots/employee_error.png"
        )

        print("Employee operation failed:", repr(e))
        print("Employee ID:", employee_id)
        print("Current URL:", driver.current_url)

        raise
