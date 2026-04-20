import os
import sys
import json
import re
import time
from datetime import datetime
from html import escape
from pathlib import Path
from urllib.parse import urlparse

import pytest
from config import BASE_URL
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from utils.account_api import create_authenticated_account
from utils.browser_audit import format_browser_logs, get_browser_logs, split_browser_logs
from utils.store_api import seed_cart_with_featured_product
from webdriver_manager.chrome import ChromeDriverManager

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def is_dashboard_headless_run() -> bool:
    return os.environ.get("DASHBOARD_HEADLESS", "").strip().lower() in {"1", "true", "yes", "on"}


def get_chromedriver_path():
    installed_path = Path(ChromeDriverManager().install())

    if installed_path.name.lower() == "chromedriver.exe":
        return str(installed_path)

    fallback_path = installed_path.with_name("chromedriver.exe")
    if fallback_path.exists():
        return str(fallback_path)

    raise FileNotFoundError("Khong tim thay file chromedriver.exe")


def format_step(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    return f"[STEP {timestamp}] {message}"


def _safe_artifact_name(value: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "_", value).strip("._")
    return sanitized or "artifact"


def _load_font(size: int = 16, bold: bool = False):
    candidates = [
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\seguisb.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def _wrapped_lines(text: str, width: int = 92) -> list[str]:
    if text is None:
        return [""]
    lines: list[str] = []
    for raw_line in str(text).splitlines() or [""]:
        line = raw_line.strip()
        if not line:
            lines.append("")
            continue
        while len(line) > width:
            lines.append(line[:width])
            line = line[width:]
        lines.append(line)
    return lines or [""]


def _failure_summary_lines(detail: str) -> list[str]:
    assertion_lines = []
    fallback_lines = []
    for raw_line in detail.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if "AssertionError:" in line:
            assertion_lines.append("Tóm tắt lỗi: " + line.split("AssertionError:", 1)[1].strip())
        elif line.startswith("assert "):
            assertion_lines.append("Điều kiện assert không đạt: " + line)
        elif line.startswith(("E       ", "E   ")):
            cleaned = line.removeprefix("E       ").removeprefix("E   ").strip()
            if cleaned.startswith("assert "):
                continue
            assertion_lines.append(cleaned)
        elif len(fallback_lines) < 4 and not line.startswith(("File ", ">", "_ _", "case =", "request =", "step_logger =")):
            fallback_lines.append(line)
    return assertion_lines[:12] or fallback_lines or ["Không lấy được thông tin lỗi rút gọn. Xem traceback đầy đủ trong HTML report."]


def _evidence_lines(item, detail: str) -> list[str]:
    context = getattr(item, "evidence_context", {}) or {}
    step_logs = getattr(item, "step_logs", []) or []
    lines = [
        f"Test case: {context.get('code', item.name)}",
        f"Mô tả: {context.get('scenario', item.name)}",
    ]
    if context.get("action"):
        lines.append(f"Dữ liệu / thao tác: {context['action']}")
    form_data = context.get("form_data") or {}
    if form_data:
        lines.append("Dữ liệu form đầy đủ:")
        for key, value in list(form_data.items())[:8]:
            lines.append(f"- {key}: {value if value != '' else '(trống)'}")
    if context.get("expected"):
        lines.append(f"Kết quả mong đợi: {context['expected']}")
    if step_logs:
        lines.append("Các bước đã chạy:")
        lines.extend(f"- {step}" for step in step_logs[-5:])
    lines.append("Kết quả thực tế:")
    lines.extend(_failure_summary_lines(detail)[:8])
    return lines


def _draw_lines(draw: ImageDraw.ImageDraw, lines: list[str], x: int, y: int, max_y: int, color=(230, 237, 243), font=None) -> int:
    font = font or _load_font(16)
    for line in lines:
        for segment in _wrapped_lines(line):
            fill = (248, 113, 113) if segment.startswith(("Tóm tắt lỗi:", "Điều kiện assert", "Kết quả thực tế")) else color
            draw.text((x, y), segment, fill=fill, font=font)
            y += 22
            if y > max_y:
                return y
    return y


def _compose_web_evidence_image(target_path: Path, title: str, detail: str, item) -> None:
    screenshot = Image.open(target_path).convert("RGB")
    screenshot.thumbnail((1180, 620))

    panel_height = 360
    width = max(1280, screenshot.width)
    height = screenshot.height + panel_height
    image = Image.new("RGB", (width, height), color=(14, 20, 28))
    image.paste(screenshot, (0, 0))

    draw = ImageDraw.Draw(image)
    title_font = _load_font(18, bold=True)
    body_font = _load_font(16)
    panel_top = screenshot.height
    draw.rectangle((0, panel_top, width, height), fill=(15, 23, 42))
    draw.text((28, panel_top + 20), f"Bằng chứng lỗi trên web - {title}"[:150], fill=(255, 255, 255), font=title_font)

    browser_url = getattr(item, "evidence_url", "") or BASE_URL
    draw.text((28, panel_top + 48), f"URL chụp màn hình: {browser_url}", fill=(125, 211, 252), font=body_font)

    _draw_lines(
        draw,
        _evidence_lines(item, detail),
        x=28,
        y=panel_top + 82,
        max_y=height - 24,
        font=body_font,
    )
    image.save(target_path)


def _fill_evidence_form(driver, context: dict) -> None:
    form_kind = (context or {}).get("form_kind", "")
    form_data = (context or {}).get("form_data", {}) or {}
    if not form_data:
        return

    if form_kind == "register":
        driver.execute_script(
            """
            const normalize = (text) => (text || '')
              .toString()
              .normalize('NFD')
              .replace(/[\\u0300-\\u036f]/g, '')
              .toLowerCase()
              .trim();
            const candidates = [...document.querySelectorAll('button,a,span,p,strong,b,div')]
              .map((el) => ({ el, text: normalize(el.innerText || el.textContent || '') }))
              .filter((item) => item.text === 'dang ky' || item.text === 'register' || item.text === 'sign up')
              .sort((a, b) => a.text.length - b.text.length);
            const clickable = candidates[0];
            if (clickable) clickable.el.click();
            """
        )
        time.sleep(0.8)

    driver.execute_script(
        """
        const data = arguments[0] || {};
        const normalize = (text) => (text || '')
          .toString()
          .normalize('NFD')
          .replace(/[\\u0300-\\u036f]/g, '')
          .toLowerCase();
        const fields = [...document.querySelectorAll('input, textarea, select')];
        const nativeValue = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value');
        const nativeTextAreaValue = Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype, 'value');
        const aliases = {
          fullName: ['fullname', 'full name', 'ho ten', 'ho va ten'],
          username: ['username', 'ten dang nhap', 'tai khoan', 'account'],
          email: ['email', 'mail'],
          phone: ['phone', 'so dien thoai', 'sdt', 'telephone'],
          usernameOrPhone: ['username', 'phone', 'ten dang nhap', 'so dien thoai', 'tai khoan', 'email'],
          password: ['password', 'mat khau'],
          confirmPassword: ['confirm', 're-password', 'repassword', 'nhap lai', 'xac nhan'],
          currentPassword: ['current', 'old', 'hien tai', 'cu'],
          newPassword: ['new', 'moi'],
          address: ['address', 'dia chi', 'detail'],
          detail: ['detail', 'dia chi chi tiet', 'so nha', 'thon lang'],
          notes: ['notes', 'ghi chu', 'note'],
          province: ['province', 'tinh', 'thanh pho', 'tinh thanh'],
          district: ['district', 'quan', 'huyen'],
          ward: ['ward', 'phuong', 'xa'],
          paymentMethod: ['payment', 'phuong thuc thanh toan', 'cod'],
          voucher: ['voucher', 'coupon', 'ma giam gia'],
          quantity: ['quantity', 'so luong']
        };
        function score(el, key) {
          const haystack = normalize([
            el.name, el.id, el.type, el.placeholder, el.getAttribute('aria-label'),
            el.previousElementSibling && el.previousElementSibling.innerText,
            el.parentElement && el.parentElement.innerText
          ].filter(Boolean).join(' '));
          return (aliases[key] || [key]).some((token) => haystack.includes(normalize(token)));
        }
        function setValue(el, value) {
          if (!el || value === undefined || value === null) return;
          const descriptor = el.tagName === 'TEXTAREA' ? nativeTextAreaValue : nativeValue;
          if (descriptor && descriptor.set) descriptor.set.call(el, value);
          else el.value = value;
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          el.style.outline = '3px solid #22d3ee';
          el.style.backgroundColor = '#fff7cc';
        }
        const used = new Set();
        for (const [key, value] of Object.entries(data)) {
          if (['token', 'items', 'product', 'size', 'color', 'paymentMethod'].includes(key)) continue;
          const target = fields.find((el) => !used.has(el) && score(el, key));
          if (target) used.add(target);
          setValue(target, value);
        }
        const note = document.createElement('div');
        note.setAttribute('data-codex-evidence', 'true');
        note.style.cssText = 'position:fixed;right:24px;top:96px;z-index:999999;width:420px;max-height:520px;overflow:auto;padding:18px;border-radius:16px;background:#0f172a;color:#e5e7eb;border:2px solid #22d3ee;font:15px Arial;box-shadow:0 20px 60px rgba(0,0,0,.35)';
        note.innerHTML = '<b style="color:#67e8f9">Dữ liệu test được điền/chụp bằng chứng</b><br>' +
          Object.entries(data).map(([k, v]) => `<div style="margin-top:6px"><b>${k}</b>: ${String(v || '(trống)').replaceAll('<','&lt;')}</div>`).join('');
        document.body.appendChild(note);
        """,
        form_data,
    )
    time.sleep(0.5)


def _capture_web_context_screenshot(target_path: Path, url: str, context: dict | None = None) -> bool:
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1600,1000")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    fallback_driver = None
    try:
        fallback_driver = webdriver.Chrome(
            service=Service(get_chromedriver_path()),
            options=chrome_options,
        )
        fallback_driver.set_page_load_timeout(30)
        fallback_driver.get(BASE_URL)
        target = urlparse(url)
        base = urlparse(BASE_URL)
        if target.path and target.path not in {"", "/"} and target.netloc == base.netloc:
            route = target.path
            fallback_driver.execute_script(
                "window.history.pushState({}, '', arguments[0]);"
                "window.dispatchEvent(new PopStateEvent('popstate'));",
                route,
            )
            time.sleep(1)
        _fill_evidence_form(fallback_driver, context or {})
        fallback_driver.save_screenshot(str(target_path))
        return target_path.exists()
    except Exception as exc:  # noqa: BLE001
        print(f"[Artifact] Khong the chup web context screenshot: {exc}", flush=True)
        return False
    finally:
        if fallback_driver is not None:
            try:
                fallback_driver.quit()
            except Exception:
                pass


def _create_text_evidence_image(target_path: Path, title: str, detail: str) -> None:
    width = 1280
    height = 720
    image = Image.new("RGB", (width, height), color=(14, 20, 28))
    draw = ImageDraw.Draw(image)
    title_font = _load_font(18, bold=True)
    body_font = _load_font(16)

    title_text = f"Bang chung loi tu dong - {title}"[:120]
    useful_lines = _failure_summary_lines(detail)
    detail_text = "\n".join(
        [
            "Muc dich: giup test lai thu cong nhanh hon, khong can doc toan bo traceback.",
            "Ket qua: testcase khong dat.",
            *useful_lines[:12],
        ]
    )[:2500]

    y = 36
    for line in [title_text, "", *detail_text.splitlines()]:
        wrapped = [line[i:i + 92] for i in range(0, len(line), 92)] or [""]
        for segment in wrapped:
            fill = (248, 113, 113) if segment.startswith(("Tom tat loi:", "Dieu kien assert")) else (230, 237, 243)
            draw.text((36, y), segment, fill=fill, font=title_font if y == 36 else body_font)
            y += 24
            if y > height - 48:
                break
        if y > height - 48:
            break

    image.save(target_path)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report_path = reports_dir / f"report_{timestamp}.html"
    xml_report_path = reports_dir / f"results_{timestamp}.xml"
    artifacts_dir = reports_dir / f"artifacts_{timestamp}"
    screenshots_dir = artifacts_dir / "screenshots"
    artifacts_index_path = reports_dir / f"artifacts_{timestamp}.json"

    screenshots_dir.mkdir(parents=True, exist_ok=True)

    config.option.htmlpath = str(html_report_path)
    config.option.xmlpath = str(xml_report_path)
    config._generated_report_paths = {
        "html": html_report_path,
        "xml": xml_report_path,
        "artifacts_dir": artifacts_dir,
        "screenshots_dir": screenshots_dir,
        "artifacts_index": artifacts_index_path,
    }
    config._run_artifacts = {
        "screenshots": {},
    }

    if hasattr(config, "_metadata"):
        config._metadata["Project"] = "Guangli Shop Selenium Demo"
        config._metadata["Base URL"] = "https://guangli-shop.netlify.app/"
        config._metadata["Reports"] = f"{html_report_path}, {xml_report_path}"
        config._metadata["Browser Mode"] = "Headless (dashboard)" if is_dashboard_headless_run() else "Visible (local)"


@pytest.fixture
def driver(request):
    chrome_options = Options()
    if is_dashboard_headless_run():
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--window-size=1600,1000")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
    else:
        chrome_options.add_argument("--start-maximized")
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    driver = webdriver.Chrome(
        service=Service(get_chromedriver_path()),
        options=chrome_options,
    )
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)
    request.node.driver = driver

    yield driver

    driver.quit()


@pytest.fixture
def step_logger(request):
    request.node.step_logs = []

    def log_step(message):
        step = format_step(message)
        request.node.step_logs.append(step)
        print(step, flush=True)

    return log_step


@pytest.fixture
def audit_logger(request):
    request.node.audit_logs = []

    def log_audit(title, details):
        request.node.audit_logs.append((title, details))

    return log_audit


def load_authenticated_storage(driver, authenticated_account, checkout_data_json=None):
    driver.get(BASE_URL)
    driver.execute_script(
        """
        sessionStorage.setItem('token', arguments[0]);
        sessionStorage.setItem('user', arguments[1]);
        if (arguments[2]) {
            localStorage.setItem('checkoutData', arguments[2]);
        } else {
            localStorage.removeItem('checkoutData');
        }
        """,
        authenticated_account.token,
        authenticated_account.storage_user_json,
        checkout_data_json,
    )
    driver.refresh()


@pytest.fixture
def authenticated_session(driver):
    authenticated_account = create_authenticated_account()
    load_authenticated_storage(driver, authenticated_account)
    return authenticated_account


@pytest.fixture
def seeded_cart_session(driver):
    authenticated_account = create_authenticated_account()
    seeded_cart = seed_cart_with_featured_product(authenticated_account)
    load_authenticated_storage(driver, authenticated_account)
    return authenticated_account, seeded_cart


@pytest.fixture
def seeded_checkout_session(driver):
    authenticated_account = create_authenticated_account()
    seeded_cart = seed_cart_with_featured_product(authenticated_account)
    load_authenticated_storage(driver, authenticated_account, seeded_cart.checkout_data_json)
    return authenticated_account, seeded_cart


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    extras = getattr(report, "extras", [])
    pytest_html = item.config.pluginmanager.getplugin("html")

    step_logs = getattr(item, "step_logs", [])
    if pytest_html and step_logs:
        step_items = "".join(f"<li>{escape(step)}</li>" for step in step_logs)
        extras.append(pytest_html.extras.html(f"<div><strong>Test steps</strong><ul>{step_items}</ul></div>"))

    audit_logs = getattr(item, "audit_logs", [])
    if pytest_html and audit_logs:
        audit_blocks = "".join(
            f"<li><strong>{escape(title)}</strong><pre>{escape(details)}</pre></li>"
            for title, details in audit_logs
        )
        extras.append(pytest_html.extras.html(f"<div><strong>Audit details</strong><ul>{audit_blocks}</ul></div>"))

    if report.failed:
        screenshot_path = None
        screenshots_dir = getattr(item.config, "_generated_report_paths", {}).get("screenshots_dir")
        screenshot_filename = f"{_safe_artifact_name(item.nodeid)}.png"
        if screenshots_dir:
            screenshot_path = Path(screenshots_dir) / screenshot_filename

        if hasattr(item, "driver") and screenshot_path:
            try:
                item.evidence_url = item.driver.current_url
                item.driver.save_screenshot(str(screenshot_path))
            except Exception as exc:  # noqa: BLE001
                print(f"[Artifact] Khong the luu screenshot file: {exc}", flush=True)
                screenshot_path = None

        detail = getattr(report, "longreprtext", "") or str(report.longrepr)
        if screenshot_path and not screenshot_path.exists():
            evidence_url = getattr(item, "evidence_url", BASE_URL) or BASE_URL
            evidence_context = getattr(item, "evidence_context", {}) or {}
            _capture_web_context_screenshot(screenshot_path, evidence_url, evidence_context)

        if screenshot_path and screenshot_path.exists():
            try:
                _compose_web_evidence_image(
                    screenshot_path,
                    title=f"testcase {item.name}",
                    detail=detail,
                    item=item,
                )
            except Exception as exc:  # noqa: BLE001
                print(f"[Artifact] Khong the ghep thong tin vao screenshot: {exc}", flush=True)

        if screenshot_path and not screenshot_path.exists():
            _create_text_evidence_image(
                screenshot_path,
                title=f"testcase {item.name}",
                detail=detail,
            )

        if screenshot_path and screenshot_path.exists():
            module_names = {item.module.__name__}
            if not item.module.__name__.startswith("tests."):
                module_names.add(f"tests.{item.module.__name__}")
            screenshot_entry = {
                "path": str(screenshot_path),
                "filename": screenshot_filename,
            }
            for module_name in module_names:
                lookup_key = f"{module_name}::{item.name}"
                item.config._run_artifacts.setdefault("screenshots", {})[lookup_key] = screenshot_entry

        if pytest_html and hasattr(item, "driver"):
            screenshot = item.driver.get_screenshot_as_base64()
            extras.append(pytest_html.extras.png(screenshot, "Screenshot when test failed"))
            browser_logs = get_browser_logs(item.driver)
            actionable_logs, informational_logs = split_browser_logs(browser_logs)
            if actionable_logs or informational_logs:
                browser_log_html = (
                    "<div><strong>Browser console logs</strong>"
                    f"<pre>{escape(format_browser_logs(actionable_logs + informational_logs))}</pre></div>"
                )
                extras.append(pytest_html.extras.html(browser_log_html))
        if pytest_html and screenshot_path:
            extras.append(pytest_html.extras.html(f"<div><strong>Screenshot file</strong><pre>{escape(str(screenshot_path))}</pre></div>"))

    report.extras = extras


def pytest_sessionfinish(session, exitstatus):
    """Auto-generate Excel report after the test run completes."""
    try:
        report_paths = getattr(session.config, "_generated_report_paths", {})
        xml_path = report_paths.get("xml")
        artifacts_index = report_paths.get("artifacts_index")
        run_artifacts = getattr(session.config, "_run_artifacts", {})
        if artifacts_index:
            Path(artifacts_index).write_text(
                json.dumps(run_artifacts, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        if xml_path and Path(xml_path).exists():
            from utils.excel_reporter import generate_report
            generate_report(xml_path)
    except Exception as exc:  # noqa: BLE001
        print(f"\n[Excel Report] Loi khi tao Excel: {exc}")
