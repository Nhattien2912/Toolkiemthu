import json
import subprocess
import sys
from ast import FunctionDef, parse
from pathlib import Path


CATALOG_PATH = Path(__file__).resolve().parent.parent / "catalog" / "web_test_catalog.json"
TESTS_DIR = Path(__file__).resolve().parent.parent / "tests"


def load_catalog():
    with CATALOG_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def flatten_catalog():
    catalog = load_catalog()
    flattened = []

    for category in catalog["categories"]:
        for index, item in enumerate(category["items"], start=1):
            flattened.append(
                {
                    "id": f"{category['key']}-{index:03d}",
                    "category": category["title"],
                    "title": item,
                }
            )

    return flattened


def summarize_catalog():
    catalog = load_catalog()
    total = 0
    lines = []

    for category in catalog["categories"]:
        count = len(category["items"])
        total += count
        lines.append(f"{category['key']}: {category['title']} ({count})")

    lines.append(f"CATALOG TOTAL: {total}")
    lines.append(f"AUTOMATED PYTEST FUNCTIONS: {count_automated_pytest_functions()}")
    lines.append(f"COLLECTED PYTEST CASES: {count_collected_pytest_cases()}")
    return "\n".join(lines)


def count_automated_pytest_functions():
    total = 0

    for file_path in TESTS_DIR.glob("test_*.py"):
        module = parse(file_path.read_text(encoding="utf-8"))
        total += sum(
            1
            for node in module.body
            if isinstance(node, FunctionDef) and node.name.startswith("test_")
        )

    return total


def count_collected_pytest_cases():
    command = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
    result = subprocess.run(
        command,
        cwd=TESTS_DIR.parent,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
        check=False,
    )

    return sum(1 for line in result.stdout.splitlines() if line.lstrip().startswith("<Function "))


if __name__ == "__main__":
    print(summarize_catalog())
