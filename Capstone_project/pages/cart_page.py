from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ROWS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    ROW_PRODUCT_NAME = (By.CSS_SELECTOR, "td.cart_description h4 a")
    ROW_QUANTITY = (By.CSS_SELECTOR, "td.cart_quantity button")
    ROW_TOTAL_PRICE = (By.CSS_SELECTOR, "td.cart_total p.cart_total_price")

    def go_to_cart_page(self, base_url):
        self.open(f"{base_url}/view_cart")

    def get_cart_line_items(self):
        """Returns a list of dicts: [{'name':..., 'quantity':..., 'total_price':...}, ...]"""
        rows = self.find_all(self.CART_ROWS)
        items = []
        for row in rows:
            try:
                name = row.find_element(*self.ROW_PRODUCT_NAME).text
                quantity = row.find_element(*self.ROW_QUANTITY).text
                total_price = row.find_element(*self.ROW_TOTAL_PRICE).text
                items.append({"name": name, "quantity": quantity, "total_price": total_price})
            except Exception:
                continue
        return items

    def is_product_in_cart(self, product_name: str, expected_quantity: str) -> bool:
        for item in self.get_cart_line_items():
            if item["name"].strip() == product_name.strip() and item["quantity"].strip() == expected_quantity.strip():
                return True
        return False
