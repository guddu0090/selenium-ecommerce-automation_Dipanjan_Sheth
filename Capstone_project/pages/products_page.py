from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.popup_handler import close_continue_shopping_modal_if_present


class ProductsPage(BasePage):
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    SEARCHED_PRODUCTS_HEADER = (By.XPATH, "//h2[text()='Searched Products']")
    FIRST_PRODUCT_VIEW_LINK = (
        By.XPATH,
        "(//div[@class='product-image-wrapper']//a[contains(@href,'/product_details/')])[1]",
    )

    def go_to_products_page(self, base_url):
        self.open(f"{base_url}/products")

    def search_product(self, product_name: str):
        self.type_text(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)

    def has_search_results(self) -> bool:
        return self.is_visible(self.SEARCHED_PRODUCTS_HEADER, timeout=10)

    def open_first_search_result(self):
        self.click(self.FIRST_PRODUCT_VIEW_LINK)


class ProductDetailsPage(BasePage):
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-information h2")
    QUANTITY_INPUT = (By.ID, "quantity")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".product-information button.cart")

    def get_product_name(self):
        return self.get_text(self.PRODUCT_NAME)

    def set_quantity(self, quantity: str):
        el = self.find(self.QUANTITY_INPUT)
        el.clear()
        el.send_keys(quantity)

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)
        # Site shows a Bootstrap "Added!" modal, not a native alert - dismiss it.
        close_continue_shopping_modal_if_present(self.driver)
