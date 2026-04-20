import pytest

from pages.home_page import HomePage
from pages.search_page import SearchPage


MATCHING_KEYWORDS = ["Adidas", "Nike", "Gi\u00e0y T\u00e2y"]

NO_RESULT_KEYWORDS = [
    "zzzzzzzz_not_found_12345",
    "selenium_keyword_not_found_2026",
]


@pytest.mark.parametrize("keyword", MATCHING_KEYWORDS)
def test_search_with_matching_keyword(driver, step_logger, keyword):
    home_page = HomePage(driver)
    search_page = SearchPage(driver)

    step_logger("Mo trang chu.")
    home_page.open()

    step_logger(f"Tim kiem voi tu khoa co ket qua: {keyword}.")
    home_page.search(keyword)
    search_page.wait_until_loaded()

    step_logger("Kiem tra trang search hien thi ket qua.")
    assert search_page.get_visible_product_links_count() > 0


@pytest.mark.parametrize("keyword", NO_RESULT_KEYWORDS)
def test_search_with_no_result_keyword(driver, step_logger, keyword):
    home_page = HomePage(driver)
    search_page = SearchPage(driver)

    step_logger("Mo trang chu.")
    home_page.open()

    step_logger(f"Tim kiem voi tu khoa khong co ket qua: {keyword}.")
    home_page.search(keyword)
    search_page.wait_until_loaded()

    step_logger("Kiem tra trang search hien thi trang thai khong co du lieu.")
    assert search_page.get_visible_product_links_count() == 0
