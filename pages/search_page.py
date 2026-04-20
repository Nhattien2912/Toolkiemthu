from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class SearchPage:
    PRODUCT_LINKS = (By.CSS_SELECTOR, "a[href*='/product/']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def wait_until_loaded(self):
        self.wait.until(lambda driver: driver.current_url.endswith("/search") and "SẢN PHẨM BẠN TÌM KIẾM" in self.get_body_text())

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_text(self, text):
        return text in self.get_body_text()

    def get_visible_product_links_count(self):
        return len([link for link in self.driver.find_elements(*self.PRODUCT_LINKS) if link.is_displayed()])
