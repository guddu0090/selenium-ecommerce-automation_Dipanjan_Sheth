from selenium.common.exceptions import NoAlertPresentException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait


def handle_js_alert_if_present(driver, accept: bool = True, timeout: int = 3):
    """Waits briefly for a native JS alert/confirm/prompt; accepts or dismisses it."""
    try:
        WebDriverWait(driver, timeout).until(lambda d: d.switch_to.alert)
        alert = driver.switch_to.alert
        text = alert.text
        alert.accept() if accept else alert.dismiss()
        return text
    except (TimeoutException, NoAlertPresentException):
        return None


def close_continue_shopping_modal_if_present(driver, timeout: int = 5):
    """
    automationexercise.com shows a Bootstrap modal ("Added!") after Add to Cart
    with a 'Continue Shopping' button - not a native alert, so it needs its own
    handling separate from handle_js_alert_if_present().
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC

    try:
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Continue Shopping']"))
        )
        button.click()
        return True
    except TimeoutException:
        return False
