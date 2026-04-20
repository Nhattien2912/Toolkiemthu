from __future__ import annotations

from urllib.parse import urlparse

import requests


IGNORED_WARNING_PATTERNS = (
    "React Router Future Flag Warning",
    "Swiper Loop Warning",
)


def get_browser_logs(driver) -> list[dict]:
    try:
        raw_logs = driver.get_log("browser")
    except Exception:  # noqa: BLE001
        return []

    normalized = []
    for entry in raw_logs:
        normalized.append(
            {
                "level": entry.get("level", ""),
                "message": entry.get("message", "").strip(),
                "source": entry.get("source", ""),
                "timestamp": entry.get("timestamp"),
            }
        )
    return normalized


def split_browser_logs(logs: list[dict]) -> tuple[list[dict], list[dict]]:
    actionable = []
    informational = []

    for entry in logs:
        message = entry["message"]
        level = entry["level"]

        if level == "SEVERE":
            actionable.append(entry)
            continue

        if any(pattern in message for pattern in IGNORED_WARNING_PATTERNS):
            informational.append(entry)
            continue

        if level == "WARNING":
            informational.append(entry)

    return actionable, informational


def format_browser_logs(logs: list[dict]) -> str:
    if not logs:
        return "No browser issues found."
    return "\n".join(f"[{entry['level']}] {entry['message']}" for entry in logs)


def get_visible_broken_images(driver) -> list[str]:
    return driver.execute_script(
        """
        return Array.from(document.images)
            .filter((img) => {
                const visible = !!(img.offsetWidth || img.offsetHeight || img.getClientRects().length);
                return visible && (!img.complete || img.naturalWidth === 0);
            })
            .map((img) => img.currentSrc || img.src || '(missing src)');
        """
    )


def get_same_origin_links(driver) -> list[str]:
    links = driver.execute_script(
        """
        return Array.from(document.querySelectorAll('a[href]'))
            .map((anchor) => anchor.href)
            .filter(Boolean);
        """
    )

    current_origin = urlparse(driver.current_url).netloc
    unique_links: list[str] = []
    seen: set[str] = set()
    for link in links:
        parsed = urlparse(link)
        if parsed.scheme not in {"http", "https"}:
            continue
        if parsed.netloc != current_origin:
            continue
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if normalized not in seen:
            seen.add(normalized)
            unique_links.append(normalized)
    return unique_links


def find_same_origin_links_with_bad_status(driver, *, timeout: int = 15, limit: int | None = None) -> list[dict]:
    broken_links = []
    links = get_same_origin_links(driver)
    if limit is not None:
        links = links[:limit]

    session = requests.Session()
    session.headers.update({"User-Agent": "testwebtool-browser-audit/1.0"})
    for link in links:
        try:
            response = session.get(link, timeout=timeout, allow_redirects=True)
            if response.status_code >= 400:
                broken_links.append({"url": link, "status_code": response.status_code})
        except requests.RequestException as exc:
            broken_links.append({"url": link, "status_code": "REQUEST_ERROR", "error": str(exc)})
    return broken_links


def format_link_failures(link_failures: list[dict]) -> str:
    if not link_failures:
        return "No broken direct links found."
    lines = []
    for item in link_failures:
        if "error" in item:
            lines.append(f"{item['url']} -> {item['status_code']} ({item['error']})")
        else:
            lines.append(f"{item['url']} -> {item['status_code']}")
    return "\n".join(lines)
