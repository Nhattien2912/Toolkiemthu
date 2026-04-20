import pytest

from pages.home_page import HomePage
from utils.site_api import get_nav_category_names


def normalize_labels(labels):
    return [label.casefold() for label in labels]


try:
    NAV_CATEGORY_LABELS = ["T\u1ea5t C\u1ea3", *get_nav_category_names()]
except Exception:
    NAV_CATEGORY_LABELS = [
        "T\u1ea5t C\u1ea3",
        "Gi\u00e0y Th\u1eddi Trang N\u1eef",
        "Gi\u00e0y tr\u1ebb em",
        "Gi\u00e0y Th\u1eddi Trang Nam",
        "D\u00e9p Nam",
        "Gi\u00e0y T\u00e2y",
        "Boot Nam",
    ]


@pytest.mark.parametrize(
    ("section_name", "section_index"),
    [("featured", 0), ("new", 1)],
)
def test_homepage_filter_labels_match_api_categories(driver, step_logger, section_name, section_index):
    home_page = HomePage(driver)

    step_logger(f"Mo trang chu de kiem tra danh sach tab cua section {section_name}.")
    home_page.open()

    actual_labels = home_page.get_filter_tab_labels(section_index)
    assert normalize_labels(actual_labels) == normalize_labels(NAV_CATEGORY_LABELS)
    step_logger(f"Xac nhan section {section_name} hien thi day du tab danh muc.")


@pytest.mark.parametrize("label", NAV_CATEGORY_LABELS)
def test_homepage_featured_tabs_can_be_selected(driver, step_logger, label):
    home_page = HomePage(driver)

    step_logger("Mo trang chu va thao tac tab trong section san pham noi bat.")
    home_page.open()
    home_page.click_filter_tab(0, label)

    assert home_page.get_selected_filter_tab_label(0).casefold() == label.casefold()
    assert home_page.section_has_products_or_empty_state(0)
    step_logger(f"Xac nhan tab noi bat '{label}' hoat dong va section khong bi vo.")


@pytest.mark.parametrize("label", NAV_CATEGORY_LABELS)
def test_homepage_new_tabs_can_be_selected(driver, step_logger, label):
    home_page = HomePage(driver)

    step_logger("Mo trang chu va thao tac tab trong section san pham moi.")
    home_page.open()
    home_page.click_filter_tab(1, label)

    assert home_page.get_selected_filter_tab_label(1).casefold() == label.casefold()
    assert home_page.section_has_products_or_empty_state(1)
    step_logger(f"Xac nhan tab san pham moi '{label}' hoat dong va section khong bi vo.")
