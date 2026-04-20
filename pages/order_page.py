from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class OrderPage:
    TITLE_TEXT = "Danh S\u00e1ch \u0110\u01a1n H\u00e0ng"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def open_spa(self):
        self.driver.execute_script(
            "window.history.pushState({}, '', '/my-order'); window.dispatchEvent(new PopStateEvent('popstate'));"
        )
        self.wait_until_loaded()

    def wait_until_loaded(self):
        self.wait.until(lambda driver: driver.current_url.endswith("/my-order") and self.TITLE_TEXT in self.get_body_text())

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text
