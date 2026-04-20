from utils.test_catalog import flatten_catalog, load_catalog
from utils.project_doc_data import (
    BASE37_CASE_CODES,
    EXTENDED80_CASE_CODES,
    TEST_CASE_GROUPS,
    TEST_CASE_SUMMARY,
    TIEN_TEST_CASES,
    TIEN_TEST_CASE_CODES,
)


def test_catalog_has_expected_structure():
    catalog = load_catalog()

    assert "categories" in catalog
    assert len(catalog["categories"]) > 0
    assert len(catalog["execution_notes"]) > 0


def test_catalog_ids_are_unique_and_large_enough():
    flattened = flatten_catalog()
    ids = [item["id"] for item in flattened]

    assert len(flattened) >= 180
    assert len(ids) == len(set(ids))


def test_project_doc_117_test_cases_are_unique():
    cases = [
        case
        for group in TEST_CASE_GROUPS
        for case in group["cases"]
    ]
    codes = [case["code"] for case in cases]
    duplicate_codes = sorted({code for code in codes if codes.count(code) > 1})

    assert len(cases) == 117
    assert TEST_CASE_SUMMARY["total_cases"] == 117
    assert not duplicate_codes, f"Duplicate project test case codes: {duplicate_codes}"


def test_project_doc_extended_80_does_not_overlap_base_37():
    all_codes = {
        case["code"]
        for group in TEST_CASE_GROUPS
        for case in group["cases"]
    }
    base_codes = set(BASE37_CASE_CODES)
    extended_codes = set(EXTENDED80_CASE_CODES)

    assert len(base_codes) == 37
    assert len(extended_codes) == 80
    assert base_codes.isdisjoint(extended_codes)
    assert base_codes | extended_codes == all_codes


def test_tien_test_cases_are_unique_and_complete():
    codes = [case["code"] for case in TIEN_TEST_CASES]

    assert len(codes) == 28
    assert codes == TIEN_TEST_CASE_CODES
    assert len(codes) == len(set(codes))
