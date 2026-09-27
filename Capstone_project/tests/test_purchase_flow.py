"""
Capstone Assignment 1: E-Commerce purchase flow automation.
Site under test: https://automationexercise.com/

Covers:
 1. Launch browser            -> driver fixture (utils/driver_factory.py)
 2. Login to application      -> LoginPage (with auto-signup fallback if account absent)
 3. Search product             -> ProductsPage.search_product
 4. Add product to cart        -> ProductDetailsPage.add_to_cart
 5. Update quantity            -> ProductDetailsPage.set_quantity (before adding to cart)
 6. Verify cart details        -> CartPage.is_product_in_cart
 7. Capture screenshots        -> utils/screenshot_util.py, called at every step
 8. Read test data from JSON   -> utils/data_reader.py
 9. Handle popup/alerts        -> utils/popup_handler.py
10. Generate execution report  -> pytest-html (see pytest.ini), report/execution_report.html
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.cart_page import CartPage
from pages.login_page import LoginPage, SignupFormPage
from pages.products_page import ProductDetailsPage, ProductsPage
from utils.data_reader import load_test_data
from utils.popup_handler import handle_js_alert_if_present
from utils.screenshot_util import capture_screenshot

DATA = load_test_data(source="json")  # switch to source="excel" to read from test_data.xlsx


def test_search_add_to_cart_and_verify(driver):
    base_url = DATA["base_url"]
    user = DATA["user"]
    signup_details = DATA["signup_details"]
    product_to_search = DATA["search_product"]
    quantity = DATA["quantity_to_set"]

    # ---------- Step 1: Launch browser & go to home page ----------
    driver.get(base_url)
    handle_js_alert_if_present(driver)
    capture_screenshot(driver, "01_home_page")

    # ---------- Step 2: Login (auto-signup on first run) ----------
    login_page = LoginPage(driver)
    login_page.go_to_login_page(base_url)
    capture_screenshot(driver, "02_login_page")

    login_page.login(user["email"], user["password"])

    if login_page.is_login_successful():
        capture_screenshot(driver, "03_login_success")
    else:
        # Account doesn't exist yet on this demo instance -> sign up, then we're auto-logged in.
        login_page.go_to_login_page(base_url)
        login_page.start_signup(user["name"], user["email"])
        capture_screenshot(driver, "03_signup_form_started")

        signup_form = SignupFormPage(driver)
        signup_form.fill_and_submit(signup_details)
        capture_screenshot(driver, "04_account_created")

        signup_form.confirm_account_created()
        assert login_page.is_login_successful(), "Login/signup did not succeed"
        capture_screenshot(driver, "05_logged_in_after_signup")

    # ---------- Step 3: Search product ----------
    products_page = ProductsPage(driver)
    products_page.go_to_products_page(base_url)
    capture_screenshot(driver, "06_products_page")

    products_page.search_product(product_to_search)
    assert products_page.has_search_results(), f"No search results for '{product_to_search}'"
    capture_screenshot(driver, "07_search_results")

    # ---------- Step 4 & 5: Open product, update quantity, add to cart ----------
    products_page.open_first_search_result()
    capture_screenshot(driver, "08_product_detail_page")

    product_detail = ProductDetailsPage(driver)
    product_name = product_detail.get_product_name()

    product_detail.set_quantity(quantity)
    capture_screenshot(driver, "09_quantity_updated")

    product_detail.add_to_cart()  # also closes the "Added!" popup internally
    capture_screenshot(driver, "10_added_to_cart")

    # ---------- Step 6: Verify cart details ----------
    cart_page = CartPage(driver)
    cart_page.go_to_cart_page(base_url)
    capture_screenshot(driver, "11_cart_page")

    line_items = cart_page.get_cart_line_items()
    assert len(line_items) > 0, "Cart is empty after add-to-cart"

    assert cart_page.is_product_in_cart(product_name, quantity), (
        f"Expected '{product_name}' with quantity {quantity} in cart, "
        f"but found: {line_items}"
    )
    capture_screenshot(driver, "12_cart_verified")
