from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def add_employee(driver, first_name, last_name, employee_id):
    wait = WebDriverWait(driver, 20)

    # Click PIM
    pim_menu = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='PIM']")
        )
    )
    pim_menu.click()

    # Click Add Employee
    add_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//a[text()='Add Employee']")
        )
    )
    add_button.click()

    # Enter employee details
    wait.until(
        EC.visibility_of_element_located(
            (By.NAME, "firstName")
        )
    ).send_keys(first_name)

    driver.find_element(
        By.NAME, "lastName"
    ).send_keys(last_name)

    # Enter Employee ID
    employee_id_field = driver.find_element(
        By.XPATH,
        "//label[text()='Employee Id']/following::input[1]"
    )

    employee_id_field.clear()
    employee_id_field.send_keys(employee_id)

    # Save employee
    driver.find_element(
        By.XPATH, "//button[@type='submit']"
    ).click()

    # Verify employee creation
    wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//h6[text()='Personal Details']")
        )
    )

    print("Employee created successfully!")

    return True