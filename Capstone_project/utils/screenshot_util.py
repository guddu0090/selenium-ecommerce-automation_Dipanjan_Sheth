import os
import time

SCREENSHOT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "screenshots"
)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


def capture_screenshot(driver, step_name: str) -> str:
    """Saves a timestamped screenshot and returns its file path."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_name = step_name.replace(" ", "_").lower()
    file_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}_{timestamp}.png")
    driver.save_screenshot(file_path)
    return file_path
