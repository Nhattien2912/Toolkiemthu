# Automation Backlog

## Automated Now

- `tests/test_login.py`
- `tests/test_ui.py`
- `tests/test_pages.py`
- `tests/test_search.py`
- `tests/test_catalog_integrity.py`

## High Priority Next

- Search flow
  - Search with valid keyword
  - Search with no-result keyword
  - Search keeps keyword on result page
- Category/listing flow
  - Open category
  - Verify product cards
  - Verify pagination/sort if stable
- Cart flow
  - Add product to cart
  - Update quantity
  - Remove product
- Contact flow
  - Submit valid message
  - Validate empty message

## Medium Priority

- Signup success by UI
- My account profile update
- My order list
- Change password
- Wishlist/favorite

## Usually Manual Or Mixed

- Cross-browser matrix
- Responsive matrix
- Performance/load
- Security deep testing
- Recovery after backend/network failure
- Full checklist execution from `catalog/web_test_catalog.json`
