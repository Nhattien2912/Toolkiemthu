from __future__ import annotations

import importlib.util
import json
import statistics
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = PROJECT_ROOT / "reports"
CATALOG_META_PATH = PROJECT_ROOT / "catalog" / "test_case_meta.py"

HIGH_PRIORITY_MODULES = (
    "test_login",
    "test_account_module",
    "test_register_module",
    "test_runtime_audit",
    "test_source_audit",
)
MEDIUM_PRIORITY_MODULES = ("test_cart_checkout_module",)
LOW_PRIORITY_MODULES = (
    "test_ui",
    "test_home_filters",
    "test_home_products",
    "test_pages",
    "test_search",
    "test_catalog_integrity",
    "test_source_conformance",
    "test_source_deep_conformance",
)

MODULE_GROUPS = {
    "Account": ("test_login", "test_account_module", "test_register_module"),
    "Cart": ("test_cart_checkout_module",),
    "Runtime": ("test_runtime_audit",),
    "Source": ("test_source_audit", "test_source_conformance", "test_source_deep_conformance"),
    "UI": ("test_ui", "test_home_filters", "test_home_products", "test_pages", "test_search", "test_catalog_integrity"),
}


def _load_test_case_meta() -> dict:
    spec = importlib.util.spec_from_file_location("dashboard_test_case_meta", CATALOG_META_PATH)
    if spec is None or spec.loader is None:
        return {}
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "TEST_CASE_META", {})


TEST_CASE_META = _load_test_case_meta()


def _parse_filename_timestamp(path: Path) -> datetime | None:
    stem = path.stem
    prefix = "results_"
    if not stem.startswith(prefix):
        return None
    timestamp_part = stem[len(prefix) :]
    try:
        return datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
    except ValueError:
        return None


def _format_timestamp_for_label(parsed: datetime | None, fallback: str) -> str:
    if parsed is None:
        return fallback
    return parsed.strftime("%d/%m %H:%M")


def _clean_error_message(raw_message: str) -> str:
    return " ".join(raw_message.split())


def _humanize_assertion_message(message: str) -> str:
    if not message:
        return ""
    for line in message.splitlines():
        cleaned = line.strip()
        if cleaned.startswith("AssertionError:"):
            return cleaned.removeprefix("AssertionError:").strip()
        if cleaned.startswith("assert "):
            continue
        if cleaned.startswith("E       AssertionError:"):
            return cleaned.removeprefix("E       AssertionError:").strip()
    return message.splitlines()[0].strip()


def _extract_error_message(node: ET.Element) -> str:
    message = node.attrib.get("message", "").strip()
    text = (node.text or "").strip()
    combined = " ".join(part for part in (message, text) if part)
    if "AssertionError:" in combined:
        return _clean_error_message(_humanize_assertion_message(combined))
    return _clean_error_message(combined)


def _match_html_report(xml_path: Path) -> str | None:
    timestamp = xml_path.stem.removeprefix("results_")
    candidate = REPORTS_DIR / f"report_{timestamp}.html"
    if candidate.exists():
        return candidate.name
    return None


def _match_excel_report(xml_path: Path) -> str | None:
    timestamp = xml_path.stem.removeprefix("results_")
    candidate = REPORTS_DIR / f"report_excel_{timestamp}.xlsx"
    if candidate.exists():
        return candidate.name

    xml_mtime = xml_path.stat().st_mtime
    excel_candidates = sorted(
        REPORTS_DIR.glob("report_excel_*.xlsx"),
        key=lambda item: abs(item.stat().st_mtime - xml_mtime),
    )
    if excel_candidates:
        closest = excel_candidates[0]
        if abs(closest.stat().st_mtime - xml_mtime) <= 180:
            return closest.name
    return None


def _load_screenshot_artifacts(xml_path: Path) -> dict:
    timestamp = xml_path.stem.removeprefix("results_")
    artifacts_index = REPORTS_DIR / f"artifacts_{timestamp}.json"
    if not artifacts_index.exists():
        return {}
    try:
        payload = json.loads(artifacts_index.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload.get("screenshots", {})


def _default_description(test_name: str) -> str:
    return test_name.replace("_", " ").strip().title()


def _lookup_meta(classname: str, name: str) -> dict:
    key = f"{classname}::{name}"
    if key in TEST_CASE_META:
        return TEST_CASE_META[key]

    for meta_key, meta_value in TEST_CASE_META.items():
        meta_name = meta_key.split("::")[-1]
        if meta_name == name or name.startswith(meta_name + "[") or name.startswith(meta_name + " "):
            return meta_value

    return {}


def _module_name_from_classname(classname: str) -> str:
    if any(name in classname for name in HIGH_PRIORITY_MODULES):
        return "Login / Account"
    if any(name in classname for name in MEDIUM_PRIORITY_MODULES):
        return "Cart / Checkout"
    if any(name in classname for name in LOW_PRIORITY_MODULES):
        return "UI / Navigation"
    return "Other"


def _module_group_from_classname(classname: str) -> str:
    for label, markers in MODULE_GROUPS.items():
        if any(marker in classname for marker in markers):
            return label
    return "Other"


def get_severity(classname: str) -> str:
    if any(name in classname for name in HIGH_PRIORITY_MODULES):
        return "HIGH"
    if any(name in classname for name in MEDIUM_PRIORITY_MODULES):
        return "MEDIUM"
    return "LOW"


def format_duration(seconds: float) -> str:
    if seconds is None:
        return "0s"
    total_seconds = int(round(float(seconds)))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    parts: list[str] = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if secs or not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)


def format_run_date(timestamp_raw: str | None, timestamp_dt: datetime | None) -> str:
    if timestamp_raw:
        try:
            return datetime.fromisoformat(timestamp_raw).strftime("%d/%m/%Y")
        except ValueError:
            pass
    if timestamp_dt is not None:
        return timestamp_dt.strftime("%d/%m/%Y")
    return datetime.now().strftime("%d/%m/%Y")


def get_health_score(pass_rate: float) -> dict:
    score = int(round(pass_rate))
    if pass_rate >= 95:
        css_class = "health-green"
    elif pass_rate >= 80:
        css_class = "health-yellow"
    else:
        css_class = "health-red"
    return {"score": score, "css_class": css_class}


def _short_actual_result(error_message: str) -> str:
    if not error_message:
        return "Như mong đợi"
    last_line = error_message.strip().splitlines()[-1]
    return last_line[:200]


def _build_manual_retest_steps(testcase: dict) -> list[dict]:
    raw_steps = testcase.get("steps") or []
    if not raw_steps:
        return [
            {
                "index": 1,
                "action": testcase.get("description", testcase["name"]),
                "expected": "Thực thi được testcase theo đúng điều kiện trong hệ thống hiện tại.",
                "actual": _short_actual_result(testcase.get("error_message", "")),
                "is_failure_point": True,
            }
        ]

    manual_steps = []
    total_steps = len(raw_steps)
    for index, step in enumerate(raw_steps, start=1):
        is_failure_point = testcase["status"] in {"failed", "error"} and index == total_steps
        manual_steps.append(
            {
                "index": index,
                "action": step.get("detail", ""),
                "expected": step.get("expected", ""),
                "actual": _short_actual_result(testcase.get("error_message", "")) if is_failure_point else "Như mong đợi",
                "is_failure_point": is_failure_point,
            }
        )
    return manual_steps


def _build_manual_retest_packet(testcase: dict) -> dict:
    return {
        "title": f"Test lại thủ công - {testcase['case_id']}",
        "prerequisites": testcase.get("prerequisites", []),
        "test_data": testcase.get("test_data", []),
        "steps": _build_manual_retest_steps(testcase),
        "expected_summary": "Thực hiện đủ toàn bộ bước và đạt expected ở từng bước, không phát sinh lỗi ngoài mong đợi.",
        "actual_summary": _short_actual_result(testcase.get("error_message", "")) if testcase["status"] in {"failed", "error"} else "Không có lỗi.",
    }


def build_case_sheet(run: dict, testcase: dict) -> dict:
    overall_status = testcase["status"]
    if overall_status == "passed":
        overall_label = "Pass"
        overall_class = "sheet-pass"
    elif overall_status in {"failed", "error"}:
        overall_label = "Fail"
        overall_class = "sheet-fail"
    else:
        overall_label = "Not Executed"
        overall_class = "sheet-skip"

    step_rows = []
    raw_steps = testcase.get("steps") or []
    if raw_steps:
        for index, step in enumerate(raw_steps, start=1):
            if overall_status == "passed":
                actual_result = "Như mong đợi"
                step_status = "Pass"
                status_class = "sheet-pass"
            elif overall_status in {"failed", "error"}:
                if index == len(raw_steps):
                    actual_result = _short_actual_result(testcase.get("error_message", ""))
                    step_status = "Fail"
                    status_class = "sheet-fail"
                else:
                    actual_result = "Như mong đợi"
                    step_status = "Pass"
                    status_class = "sheet-pass"
            else:
                actual_result = ""
                step_status = "Not executed"
                status_class = "sheet-skip"

            step_rows.append(
                {
                    "index": index,
                    "detail": step.get("detail", ""),
                    "expected": step.get("expected", ""),
                    "actual": actual_result,
                    "result": step_status,
                    "status_class": status_class,
                }
            )
    else:
        default_actual = "Như mong đợi" if overall_status == "passed" else _short_actual_result(testcase.get("error_message", ""))
        step_rows.append(
            {
                "index": 1,
                "detail": testcase.get("description", testcase["name"]),
                "expected": "Thực thi thành công theo metadata hiện có.",
                "actual": default_actual,
                "result": overall_label,
                "status_class": overall_class,
            }
        )

    return {
        "case_id": testcase["case_id"],
        "description": testcase["description"],
        "created_by": "Selenium Auto",
        "reviewed_by": "",
        "version": "1.0",
        "technique": testcase.get("technique", "Functional Testing"),
        "tester_name": "Selenium Auto",
        "date_tested": format_run_date(run.get("timestamp_raw"), run.get("timestamp_dt")),
        "overall_result": overall_label,
        "overall_class": overall_class,
        "prerequisites": testcase.get("prerequisites", []),
        "test_data": testcase.get("test_data", []),
        "step_rows": step_rows,
        "manual_retest_packet": _build_manual_retest_packet(testcase),
        "is_failed_case": overall_status in {"failed", "error"},
        "error_message": testcase.get("error_message", ""),
        "screenshot_relative": testcase.get("screenshot_relative"),
        "screenshot_filename": testcase.get("screenshot_filename"),
    }


def _parse_testcase(testcase: ET.Element, screenshot_artifacts: dict | None = None) -> dict:
    classname = testcase.attrib.get("classname", "")
    name = testcase.attrib.get("name", "")
    duration = float(testcase.attrib.get("time", 0.0) or 0.0)
    meta = _lookup_meta(classname, name)
    status = "passed"
    error_message = ""
    screenshot_relative = None
    screenshot_filename = None

    if screenshot_artifacts:
        artifact = screenshot_artifacts.get(f"{classname}::{name}", {})
        raw_path = artifact.get("path")
        if raw_path:
            artifact_path = Path(raw_path)
            try:
                screenshot_relative = str(artifact_path.resolve().relative_to(REPORTS_DIR.resolve())).replace("\\", "/")
                screenshot_filename = artifact_path.name
            except ValueError:
                screenshot_relative = None
                screenshot_filename = None

    child = testcase.find("failure")
    if child is not None:
        status = "failed"
        error_message = _extract_error_message(child)
    else:
        child = testcase.find("error")
        if child is not None:
            status = "error"
            error_message = _extract_error_message(child)
        else:
            child = testcase.find("skipped")
            if child is not None:
                status = "skipped"
                error_message = _extract_error_message(child)

    return {
        "classname": classname,
        "name": name,
        "lookup_key": f"{classname}::{name}",
        "time": duration,
        "time_display": format_duration(duration),
        "status": status,
        "error_message": error_message,
        "error_snippet": error_message[:200] + ("..." if len(error_message) > 200 else ""),
        "case_id": meta.get("id", "UNMAPPED"),
        "description": meta.get("description", _default_description(name)),
        "technique": meta.get("technique", "Functional Testing"),
        "prerequisites": meta.get("prerequisites", []),
        "test_data": meta.get("test_data", []),
        "steps": meta.get("steps", []),
        "severity": meta.get("severity", get_severity(classname)),
        "module_name": _module_name_from_classname(classname),
        "screenshot_relative": screenshot_relative,
        "screenshot_filename": screenshot_filename,
    }


def _parse_run(xml_path: Path) -> dict | None:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    testsuite = root.find("testsuite") if root.tag == "testsuites" else root
    if testsuite is None:
        return None

    tests = int(testsuite.attrib.get("tests", 0) or 0)
    if tests == 0:
        return None

    failures = int(testsuite.attrib.get("failures", 0) or 0)
    errors = int(testsuite.attrib.get("errors", 0) or 0)
    skipped = int(testsuite.attrib.get("skipped", 0) or 0)
    duration = float(testsuite.attrib.get("time", 0.0) or 0.0)
    timestamp_raw = testsuite.attrib.get("timestamp", "")
    filename_timestamp = _parse_filename_timestamp(xml_path)
    pass_count = max(tests - failures - errors - skipped, 0)
    executed_count = max(tests - skipped, 1)
    pass_rate = (pass_count / tests) * 100 if tests else 0.0
    average_case_time = duration / executed_count if executed_count else 0.0
    screenshot_artifacts = _load_screenshot_artifacts(xml_path)
    testcases = [_parse_testcase(testcase, screenshot_artifacts) for testcase in testsuite.findall("testcase")]

    return {
        "xml_filename": xml_path.name,
        "xml_path": str(xml_path),
        "html_filename": _match_html_report(xml_path),
        "excel_filename": _match_excel_report(xml_path),
        "timestamp_raw": timestamp_raw,
        "timestamp_dt": filename_timestamp,
        "timestamp_display": _format_timestamp_for_label(filename_timestamp, xml_path.stem),
        "tests": tests,
        "failures": failures,
        "errors": errors,
        "skipped": skipped,
        "passed": pass_count,
        "time_seconds": duration,
        "duration_display": format_duration(duration),
        "avg_time_case_seconds": average_case_time,
        "avg_time_case_display": format_duration(average_case_time),
        "pass_rate": round(pass_rate, 2),
        "health_score": get_health_score(pass_rate),
        "testcases": testcases,
    }


def get_all_runs() -> list[dict]:
    runs: list[dict] = []
    for xml_path in REPORTS_DIR.glob("results_*.xml"):
        run = _parse_run(xml_path)
        if run is not None:
            runs.append(run)
    runs.sort(key=lambda item: item["timestamp_dt"] or datetime.min, reverse=True)
    return runs


def get_latest_run() -> dict | None:
    runs = get_all_runs()
    return runs[0] if runs else None


def get_critical_failures(run: dict) -> list[dict]:
    severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    failing = []
    for index, case in enumerate(run["testcases"]):
        if case["status"] in {"failed", "error"}:
            failing.append({**case, "case_index": index})
    failing.sort(key=lambda case: (severity_rank.get(case["severity"], 99), -case["time"], case["name"]))
    return failing


def get_historical_data(runs: list[dict], n: int = 7) -> dict:
    selected = list(reversed(runs[:n]))
    labels = [run["timestamp_display"] for run in selected]
    pass_rates = [run["pass_rate"] for run in selected]
    colors = []
    for pass_rate in pass_rates:
        if pass_rate >= 95:
            colors.append("#16a34a")
        elif pass_rate >= 80:
            colors.append("#ca8a04")
        else:
            colors.append("#dc2626")

    trend = "Not enough data"
    if len(pass_rates) >= 4:
        change = pass_rates[-1] - pass_rates[0]
        volatility = statistics.pstdev(pass_rates)
        if volatility >= 12:
            trend = "Volatile"
        elif change >= 5:
            trend = "Steady Upward"
        elif change <= -5:
            trend = "Declining"
        else:
            trend = "Stable"

    return {"labels": labels, "pass_rates": pass_rates, "colors": colors, "trend": trend}


def get_automated_insights(run: dict, all_runs: list[dict]) -> str:
    current_failures = [case for case in run["testcases"] if case["status"] in {"failed", "error"}]
    if not current_failures:
        return "Latest run has no failing test cases. The suite is currently stable across the monitored modules."

    current_counter = Counter(case["module_name"] for case in current_failures)
    current_module, current_count = current_counter.most_common(1)[0]

    recent_runs = all_runs[:7]
    historical_counter: Counter[str] = Counter()
    for historical_run in recent_runs:
        for case in historical_run["testcases"]:
            if case["status"] in {"failed", "error"}:
                historical_counter[case["module_name"]] += 1

    if historical_counter:
        historical_module, historical_count = historical_counter.most_common(1)[0]
        return (
            f"Current failures are concentrated in {current_module} ({current_count} case"
            f"{'s' if current_count != 1 else ''}). Over the last {len(recent_runs)} valid runs, "
            f"{historical_module} has produced the most instability with {historical_count} failing cases."
        )

    return f"Current failures are concentrated in {current_module} ({current_count} case{'s' if current_count != 1 else ''})."


def get_module_trend_data(runs: list[dict], n: int = 10) -> dict:
    selected = list(reversed(runs[:n]))
    labels = [run["timestamp_display"] for run in selected]
    datasets = []
    palette = {
        "Account": "#2563eb",
        "Cart": "#16a34a",
        "Runtime": "#dc2626",
        "Source": "#ca8a04",
        "UI": "#8b5cf6",
    }

    for module_label in MODULE_GROUPS:
        values = []
        for run in selected:
            module_cases = [case for case in run["testcases"] if _module_group_from_classname(case["classname"]) == module_label]
            if not module_cases:
                values.append(None)
                continue
            passed = sum(1 for case in module_cases if case["status"] == "passed")
            values.append(round((passed / len(module_cases)) * 100, 2))
        datasets.append(
            {
                "label": module_label,
                "data": values,
                "borderColor": palette.get(module_label, "#9da7b3"),
                "backgroundColor": palette.get(module_label, "#9da7b3"),
            }
        )

    return {"labels": labels, "datasets": datasets}


def get_bug_tracker_rows(runs: list[dict]) -> list[dict]:
    bug_map: dict[str, dict] = {}

    for run in runs:
        for case_index, case in enumerate(run["testcases"]):
            if case["status"] not in {"failed", "error"}:
                continue
            bug_key = case["case_id"] if case["case_id"] != "UNMAPPED" else case["lookup_key"]
            row = bug_map.setdefault(
                bug_key,
                {
                    "bug_key": bug_key,
                    "case_id": case["case_id"],
                    "name": case["name"],
                    "description": case["description"],
                    "severity": case["severity"],
                    "module_name": case["module_name"],
                    "occurrences": 0,
                    "first_seen": run["timestamp_display"],
                    "last_seen": run["timestamp_display"],
                    "latest_error": case["error_snippet"] or case["error_message"],
                    "xml_filename": run["xml_filename"],
                    "case_index": case_index,
                    "prerequisites": case.get("prerequisites", []),
                    "test_data": case.get("test_data", []),
                    "manual_retest_packet": _build_manual_retest_packet(case),
                },
            )
            row["occurrences"] += 1
            row["last_seen"] = run["timestamp_display"]
            row["xml_filename"] = run["xml_filename"]
            row["case_index"] = case_index
            row["latest_error"] = case["error_snippet"] or case["error_message"]
            row["prerequisites"] = case.get("prerequisites", [])
            row["test_data"] = case.get("test_data", [])
            row["manual_retest_packet"] = _build_manual_retest_packet(case)

    severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    rows = list(bug_map.values())
    rows.sort(key=lambda row: (severity_rank.get(row["severity"], 99), -row["occurrences"], row["case_id"], row["name"]))
    return rows


def compare_runs(run_a: dict, run_b: dict) -> dict:
    map_a = {case["lookup_key"]: case for case in run_a["testcases"]}
    map_b = {case["lookup_key"]: case for case in run_b["testcases"]}
    all_keys = sorted(set(map_a) | set(map_b))

    regressions = []
    fixed = []
    unchanged_failures = []
    added = []
    removed = []

    for key in all_keys:
        case_a = map_a.get(key)
        case_b = map_b.get(key)
        status_a = case_a["status"] if case_a else "missing"
        status_b = case_b["status"] if case_b else "missing"
        case_ref = case_b or case_a
        row = {
            "lookup_key": key,
            "case_id": case_ref["case_id"],
            "name": case_ref["name"],
            "module_name": case_ref["module_name"],
            "severity": case_ref["severity"],
            "status_a": status_a,
            "status_b": status_b,
        }

        fail_a = status_a in {"failed", "error"}
        fail_b = status_b in {"failed", "error"}
        pass_a = status_a == "passed"
        pass_b = status_b == "passed"

        if status_a == "missing":
            added.append(row)
        elif status_b == "missing":
            removed.append(row)
        elif not fail_a and fail_b:
            regressions.append(row)
        elif fail_a and pass_b:
            fixed.append(row)
        elif fail_a and fail_b:
            unchanged_failures.append(row)

    severity_rank = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
    sorter = lambda row: (severity_rank.get(row["severity"], 99), row["case_id"], row["name"])
    regressions.sort(key=sorter)
    fixed.sort(key=sorter)
    unchanged_failures.sort(key=sorter)
    added.sort(key=sorter)
    removed.sort(key=sorter)

    return {
        "run_a": run_a,
        "run_b": run_b,
        "regressions": regressions,
        "fixed": fixed,
        "unchanged_failures": unchanged_failures,
        "added": added,
        "removed": removed,
    }
