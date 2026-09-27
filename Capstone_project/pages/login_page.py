from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGIN_ERROR = (By.CSS_SELECTOR, ".login-form p[style]")

    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "button[data-qa='signup-button']")

    LOGGED_IN_INDICATOR = (By.XPATH, "//a[contains(text(),'Logged in as')]")

    def go_to_login_page(self, base_url):
        self.open(f"{base_url}/login")

    def login(self, email, password):
        self.type_text(self.LOGIN_EMAIL, email)
        self.type_text(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_successful(self):
        return self.is_visible(self.LOGGED_IN_INDICATOR, timeout=6)

    def start_signup(self, name, email):
        self.type_text(self.SIGNUP_NAME, name)
        self.type_text(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)


class SignupFormPage(BasePage):
    """The 'ENTER ACCOUNT INFORMATION' page shown after starting signup."""

    TITLE_MR = (By.ID, "id_gender1")
    PASSWORD = (By.ID, "password")
    DAYS = (By.ID, "days")
    MONTHS = (By.ID, "months")
    YEARS = (By.ID, "years")
    FIRST_NAME = (By.ID, "first_name")
    LAST_NAME = (By.ID, "last_name")
    COMPANY = (By.ID, "company")
    ADDRESS1 = (By.ID, "address1")
    ADDRESS2 = (By.ID, "address2")
    COUNTRY = (By.ID, "country")
    STATE = (By.ID, "state")
    CITY = (By.ID, "city")
    ZIPCODE = (By.ID, "zipcode")
    MOBILE_NUMBER = (By.ID, "mobile_number")
    CREATE_ACCOUNT_BUTTON = (By.CSS_SELECTOR, "button[data-qa='create-account']")
    ACCOUNT_CREATED_CONTINUE = (By.CSS_SELECTOR, "a[data-qa='continue-button']")

    def fill_and_submit(self, details: dict):
        from selenium.webdriver.support.ui import Select

        self.click(self.TITLE_MR)
        self.type_text(self.PASSWORD, details["password"])
        Select(self.find(self.DAYS)).select_by_value(details["birth_day"])
        Select(self.find(self.MONTHS)).select_by_value(details["birth_month"])
        Select(self.find(self.YEARS)).select_by_value(details["birth_year"])
        self.type_text(self.FIRST_NAME, details["first_name"])
        self.type_text(self.LAST_NAME, details["last_name"])
        self.type_text(self.COMPANY, details["company"])
        self.type_text(self.ADDRESS1, details["address1"])
        self.type_text(self.ADDRESS2, details["address2"])
        Select(self.find(self.COUNTRY)).select_by_visible_text(details["country"])
        self.type_text(self.STATE, details["state"])
        self.type_text(self.CITY, details["city"])
        self.type_text(self.ZIPCODE, details["zipcode"])
        self.type_text(self.MOBILE_NUMBER, details["mobile_number"])
        self.click(self.CREATE_ACCOUNT_BUTTON)

    def confirm_account_created(self):
        self.click(self.ACCOUNT_CREATED_CONTINUE)
