from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_driver(browser: str = "chrome", headless: bool = False):
    browser = browser.lower()

    if browser == "chrome":
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        # Selenium 4.6+ resolves the matching chromedriver automatically (Selenium Manager)
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        from selenium.webdriver.firefox.options import Options as FFOptions
        ff_options = FFOptions()
        if headless:
            ff_options.add_argument("--headless")
        driver = webdriver.Firefox(options=ff_options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.implicitly_wait(5)
    if not headless:
        driver.maximize_window()
    return driver
