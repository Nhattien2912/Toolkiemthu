from config import BASE_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class HomePage:
    SEARCH_INPUT = (By.CSS_SELECTOR, "input.search-input")
    PRODUCT_LINKS = (By.CSS_SELECTOR, "a[href*='/product/']")
    CART_LINK = (By.CSS_SELECTOR, "a[href$='/cart']")
    CONTACT_LINK = (By.CSS_SELECTOR, "a[href$='/contact']")
    FILTER_TAB_LISTS = (By.CSS_SELECTOR, ".filterTabs")
    FILTER_TABS = (By.CSS_SELECTOR, "[role='tab']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 60)

    def open(self):
        self.driver.get(BASE_URL)
        self.wait.until(EC.visibility_of_element_located(self.SEARCH_INPUT))

    def get_body_text(self):
        return self.driver.find_element(By.TAG_NAME, "body").text

    def has_text(self, text):
        return text in self.get_body_text()

    def get_visible_product_links_count(self):
        return len([link for link in self.driver.find_elements(*self.PRODUCT_LINKS) if link.is_displayed()])

    def get_visible_product_titles(self):
        return [link.text.strip() for link in self.driver.find_elements(*self.PRODUCT_LINKS) if link.is_displayed() and link.text.strip()]

    def get_search_placeholder(self):
        return self.driver.find_element(*self.SEARCH_INPUT).get_attribute("placeholder")

    def click_search_button(self):
        visible_buttons = [button for button in self.driver.find_elements(By.CSS_SELECTOR, "button") if button.is_displayed()]
        if not visible_buttons:
            raise RuntimeError("Khong tim thay search button.")

        self.driver.execute_script("arguments[0].click();", visible_buttons[0])

    def open_first_product(self):
        self.open_visible_product(0)

    def open_visible_product(self, index):
        self.wait.until(lambda driver: self.get_visible_product_links_count() > 0)

        visible_links = [link for link in self.driver.find_elements(*self.PRODUCT_LINKS) if link.is_displayed() and link.text.strip()]
        if 0 <= index < len(visible_links):
            self.driver.execute_script("arguments[0].click();", visible_links[index])
            return

        raise RuntimeError("Khong tim thay product link de mo.")

    def _get_filter_tab_list(self, section_index):
        tab_lists = self.driver.find_elements(*self.FILTER_TAB_LISTS)
        if 0 <= section_index < len(tab_lists):
            return tab_lists[section_index]

        raise RuntimeError(f"Khong tim thay filter tab list thu {section_index}.")

    def _get_section_container_by_tab_list(self, tab_list):
        return tab_list.find_element(By.XPATH, "./ancestor::div[contains(@class,'row')][1]")

    def _wait_for_filter_tabs_ready(self, tab_list, min_count=7):
        self.wait.until(
            lambda driver: self.driver.execute_script(
                """
                return Array.from(arguments[0].querySelectorAll('[role="tab"]'))
                    .map((tab) => tab.textContent.trim())
                    .filter(Boolean)
                    .length;
                """,
                tab_list,
            )
            >= min_count
        )

    def get_filter_tab_labels(self, section_index):
        tab_list = self._get_filter_tab_list(section_index)
        self._wait_for_filter_tabs_ready(tab_list)
        return self.driver.execute_script(
            """
            return Array.from(arguments[0].querySelectorAll('[role="tab"]'))
                .map((tab) => tab.textContent.trim())
                .filter(Boolean);
            """,
            tab_list,
        )

    def click_filter_tab(self, section_index, label):
        tab_list = self._get_filter_tab_list(section_index)
        self._wait_for_filter_tabs_ready(tab_list)
        tab = self.driver.execute_script(
            """
            const normalizedLabel = arguments[1].trim().toLowerCase();
            const tabs = Array.from(arguments[0].querySelectorAll('[role="tab"]'));
            return tabs.find((item) => item.textContent.trim().toLowerCase() === normalizedLabel) || null;
            """,
            tab_list,
            label,
        )

        if tab is not None:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", tab)
            self.driver.execute_script("arguments[0].click();", tab)
            self.wait.until(lambda driver: tab.get_attribute("aria-selected") == "true")
            return

        raise RuntimeError(f"Khong tim thay tab: {label}")

    def get_selected_filter_tab_label(self, section_index):
        tab_list = self._get_filter_tab_list(section_index)
        for tab in tab_list.find_elements(*self.FILTER_TABS):
            if tab.is_displayed() and tab.get_attribute("aria-selected") == "true":
                return tab.text.strip()

        raise RuntimeError("Khong co filter tab nao dang duoc chon.")

    def get_section_text(self, section_index):
        container = self._get_section_container_by_tab_list(self._get_filter_tab_list(section_index))
        return container.text

    def get_section_visible_product_links_count(self, section_index):
        container = self._get_section_container_by_tab_list(self._get_filter_tab_list(section_index))
        return len(
            [
                link
                for link in container.find_elements(*self.PRODUCT_LINKS)
                if link.is_displayed() and link.text.strip()
            ]
        )

    def section_has_products_or_empty_state(self, section_index):
        section_text = self.get_section_text(section_index)
        return self.get_section_visible_product_links_count(section_index) > 0 or "Kh\u00f4ng c\u00f3 d\u1eef li\u1ec7u" in section_text

    def go_to_cart(self):
        cart_link = self.wait.until(EC.presence_of_element_located(self.CART_LINK))
        self.driver.execute_script("arguments[0].click();", cart_link)

    def go_to_contact(self):
        contact_link = self.wait.until(EC.presence_of_element_located(self.CONTACT_LINK))
        self.driver.execute_script("arguments[0].click();", contact_link)

    def search(self, keyword):
        search_input = self.driver.find_element(*self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(keyword)
        self.click_search_button()
