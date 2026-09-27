import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_factory import get_driver
from utils.screenshot_util import capture_screenshot


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    drv = get_driver(browser=browser, headless=headless)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """On failure, capture a screenshot and attach it to the pytest-html report."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        driver = item.funcargs.get("driver")
        if driver is not None:
            extra = getattr(report, "extra", [])
            try:
                from pytest_html import extras

                if report.failed:
                    path = capture_screenshot(driver, f"FAILED_{item.name}")
                else:
                    path = capture_screenshot(driver, f"PASSED_{item.name}")
                relative_path = os.path.relpath(path, os.path.dirname(os.path.abspath(__file__)))
                extra.append(extras.image(relative_path))
            except Exception:
                pass
            report.extra = extra
