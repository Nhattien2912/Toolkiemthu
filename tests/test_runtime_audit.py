from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.browser_audit import (
    find_same_origin_links_with_bad_status,
    format_browser_logs,
    format_link_failures,
    get_browser_logs,
    get_visible_broken_images,
    split_browser_logs,
)


def test_homepage_has_no_actionable_browser_console_errors(driver, step_logger, audit_logger):
    home_page = HomePage(driver)

    step_logger("Mo trang chu de audit console runtime.")
    home_page.open()

    logs = get_browser_logs(driver)
    actionable_logs, informational_logs = split_browser_logs(logs)
    audit_logger("Homepage actionable console logs", format_browser_logs(actionable_logs))
    if informational_logs:
        audit_logger("Homepage informational browser logs", format_browser_logs(informational_logs))

    assert not actionable_logs, format_browser_logs(actionable_logs)


def test_login_page_has_no_actionable_browser_console_errors(driver, step_logger, audit_logger):
    login_page = LoginPage(driver)

    step_logger("Mo trang dang nhap de audit console runtime.")
    login_page.open()

    logs = get_browser_logs(driver)
    actionable_logs, informational_logs = split_browser_logs(logs)
    audit_logger("Login actionable console logs", format_browser_logs(actionable_logs))
    if informational_logs:
        audit_logger("Login informational browser logs", format_browser_logs(informational_logs))

    assert not actionable_logs, format_browser_logs(actionable_logs)


def test_homepage_visible_images_are_not_broken(driver, step_logger, audit_logger):
    home_page = HomePage(driver)

    step_logger("Mo trang chu va audit cac hinh dang hien thi.")
    home_page.open()

    broken_images = get_visible_broken_images(driver)
    audit_logger(
        "Homepage broken visible images",
        "\n".join(broken_images) if broken_images else "No broken visible images found.",
    )

    assert not broken_images, "\n".join(broken_images)


def test_homepage_same_origin_links_are_directly_resolvable(driver, step_logger, audit_logger):
    home_page = HomePage(driver)

    step_logger("Mo trang chu va kiem tra cac same-origin link co mo truc tiep duoc hay khong.")
    home_page.open()

    broken_links = find_same_origin_links_with_bad_status(driver, limit=25)
    audit_logger("Homepage direct-route failures", format_link_failures(broken_links))

    assert not broken_links, format_link_failures(broken_links)


def test_checkout_page_has_no_actionable_browser_console_errors(driver, seeded_checkout_session, step_logger, audit_logger):
    checkout_page = CheckoutPage(driver)

    step_logger("Xoa browser logs cu de audit checkout chinh xac.")
    get_browser_logs(driver)

    step_logger("Mo trang checkout da duoc seed va audit console runtime.")
    checkout_page.open_spa()

    logs = get_browser_logs(driver)
    actionable_logs, informational_logs = split_browser_logs(logs)
    audit_logger("Checkout actionable console logs", format_browser_logs(actionable_logs))
    if informational_logs:
        audit_logger("Checkout informational browser logs", format_browser_logs(informational_logs))

    assert not actionable_logs, format_browser_logs(actionable_logs)
