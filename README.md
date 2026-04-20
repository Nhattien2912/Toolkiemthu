# Selenium Web Test Project

Project mau test web bang Python Selenium, phu hop cho sinh vien moi hoc.
Web demo dang test:

```text
https://guangli-shop.netlify.app/
```

## 1. Cai dat

Can co:
- Python 3.10+
- Google Chrome

Lenh cai thu vien:

```bash
pip install -r requirements.txt
```

Hoac cai truc tiep:

```bash
pip install selenium pytest pytest-html webdriver-manager requests flask
```

## 2. Cau truc project

```text
testwebtool/
|-- config.py
|-- conftest.py
|-- catalog/
|   `-- web_test_catalog.json
|-- docs/
|   |-- automation_backlog.md
|   `-- web_test_catalog.md
|-- dashboard.py
|-- pytest.ini
|-- requirements.txt
|-- pages/
|   |-- account_page.py
|   |-- cart_page.py
|   |-- checkout_page.py
|   |-- contact_page.py
|   |-- home_page.py
|   |-- login_page.py
|   |-- order_page.py
|   |-- product_page.py
|   `-- search_page.py
|-- reports/
|   `-- report_*.html / results_*.xml
|-- static/
|   |-- app.js
|   `-- style.css
|-- templates/
|   |-- base.html
|   |-- dashboard.html
|   |-- logs.html
|   `-- reports.html
|-- utils/
|   |-- excel_reporter.py
|   |-- report_parser.py
|   |-- site_api.py
|   |-- store_api.py
|   |-- test_catalog.py
|   `-- account_api.py
`-- tests/
    |-- test_account_module.py
    |-- test_catalog_integrity.py
    |-- test_cart_checkout_module.py
    |-- test_pages.py
    |-- test_register_module.py
    |-- test_search.py
    |-- test_ui.py
    `-- test_login.py
```

## 3. Chay test

Chay tat ca test:

```bash
pytest
```

Chay dashboard web:

```bash
py dashboard.py
```

Sau do mo:

```text
http://localhost:5050
```

Khi chay, terminal se hien tung buoc dang thuc hien theo dang:

```text
[STEP 17:10:01] Mo trang chu Guangli Shop.
[STEP 17:10:05] Kiem tra o tim kiem va cac khoi giao dien chinh.
```

Xem tong hop catalog 180+ test case:

```bash
python -m utils.test_catalog
```

Luu y quan trong:
- `catalog/web_test_catalog.json` = tong checklist 180+ case
- `tests/*.py` = so case da duoc code hoa bang pytest/Selenium
- Vi vay report pytest se hien so test automation da code, khong phai tong so item trong catalog

## 4. Noi dung test

- `test_login_success`: tu dong tao tai khoan test moi qua API, sau do dang nhap bang giao dien web
- `test_login_invalid`: test dang nhap that bai voi tai khoan sai
- `test_homepage_main_ui`: kiem tra cac thanh phan giao dien chinh cua trang chu
- `test_login_and_signup_ui`: kiem tra giao dien form dang nhap va dang ky
- `test_product_detail_page_ui`: kiem tra trang chi tiet san pham
- `test_cart_page_empty_ui`: kiem tra trang gio hang khi chua co san pham
- `test_contact_page_ui`: kiem tra trang lien he
- `test_search_with_matching_keyword`: kiem tra search co ket qua
- `test_search_with_no_result_keyword`: kiem tra search khong co ket qua
- `test_catalog_integrity`: kiem tra catalog 180+ test case da duoc dua vao project va khong bi trung ID

## 5. Report HTML

- Hien thi pass/fail
- Moi lan chay se tao file moi theo timestamp, vi du `reports/report_20260331_180119.html`
- Xuat them file ket qua XML theo timestamp, vi du `reports/results_20260331_180119.xml`
- Hien thi danh sach tung step test trong report
- Neu test fail, screenshot se duoc gan vao report

## 6. Dashboard TestOps

- `dashboard.py`: Flask app hien thi dashboard dark theme
- `/dashboard`: tong quan run history va live log
- `/reports`: xem report moi nhat
- `/reports/<xml_filename>`: xem run cu the
- `/logs`: xem log lan chay dashboard-triggered gan nhat
- `POST /run-suite`: chay pytest ngay tu giao dien web
- `GET /stream-log`: stream log realtime bang SSE

Dashboard doc report tu:
- `reports/results_*.xml`
- `catalog/test_case_meta.py`

Dashboard hien:
- health score
- total time, avg time/case
- critical failures theo severity
- chart 7 lan chay gan nhat
- run selector
- detailed case sheet tren giao dien theo form Excel mau
- nut download file HTML report
- suite selector de chon nhom test truoc khi run
- luu trang thai that cua lan dashboard-triggered gan nhat: passed, test_failures, infra_error, no_tests
- neu lan run moi loi va khong sinh XML moi, dashboard se bao ro va khong map nham sang report cu
- co them suite `Strict Runtime Audit` de bat loi console SEVERE, broken resource va deep-link 404
- co them trang `Project Word` de hien thi noi dung do an, use case, module va nut quick-run rieng theo UC/module

Phan mo rong:
- Hien tai suite tap trung vao cac flow on dinh va it flaky cua site
- Cac flow nhu `search`, `category`, `add to cart` thuc su, `checkout` co the bo sung tiep, nhung can them locator/on dinh du lieu de tranh fail gia
- Da them bo checklist tong hop va backlog tai:
  - `catalog/web_test_catalog.json`
  - `docs/web_test_catalog.md`
  - `docs/automation_backlog.md`

## 7. Doi URL web test

Project dang mac dinh dung:

```text
BASE_URL = https://guangli-shop.netlify.app/
API_BASE_URL = https://web-mern-t10-2024.onrender.com
```

Neu muon doi sang web khac, sua trong `config.py`:

```python
BASE_URL = "https://example.com"
API_BASE_URL = "https://example-api.com"
```

Hoac dung bien moi truong:

```bash
set BASE_URL=https://guangli-shop.netlify.app/
set API_BASE_URL=https://web-mern-t10-2024.onrender.com
pytest
```

Luu y:
- Trang login cua site nay la SPA, vi vay code se mo trang chu roi click nut `Dang Nhap`
- Neu doi sang web khac, can cap nhat lai locator trong file `pages/login_page.py`
