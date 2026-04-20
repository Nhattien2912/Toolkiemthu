from __future__ import annotations

import base64
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from utils.report_parser import format_duration


def _get_chromedriver_path() -> str:
    installed_path = Path(ChromeDriverManager().install())
    if installed_path.name.lower() == "chromedriver.exe":
        return str(installed_path)
    fallback_path = installed_path.with_name("chromedriver.exe")
    if fallback_path.exists():
        return str(fallback_path)
    raise FileNotFoundError("Khong tim thay file chromedriver.exe")


def _build_report_html(run: dict, critical_failures: list[dict], automated_insights: str) -> str:
    failure_rows = []
    for failure in critical_failures[:25]:
        failure_rows.append(
            f"""
            <tr>
              <td>{failure['case_id']}</td>
              <td>{failure['name']}</td>
              <td>{failure['severity']}</td>
              <td>{failure['module_name']}</td>
              <td>{(failure['error_snippet'] or 'Khong co message')[:220]}</td>
            </tr>
            """
        )

    failures_html = "\n".join(failure_rows) or """
      <tr><td colspan="5">Khong co failure nao trong lan chay nay.</td></tr>
    """

    return f"""
    <!doctype html>
    <html lang="vi">
    <head>
      <meta charset="utf-8">
      <title>PDF Report - {run['xml_filename']}</title>
      <style>
        body {{
          font-family: Arial, sans-serif;
          color: #111827;
          margin: 28px;
        }}
        h1, h2, h3 {{ margin: 0 0 12px; }}
        .eyebrow {{
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: .12em;
          color: #2563eb;
          margin-bottom: 8px;
        }}
        .header {{
          border-bottom: 2px solid #1f3864;
          padding-bottom: 14px;
          margin-bottom: 18px;
        }}
        .grid {{
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 12px;
          margin: 18px 0;
        }}
        .card {{
          border: 1px solid #cbd5e1;
          border-radius: 10px;
          padding: 12px;
          background: #f8fafc;
        }}
        .card span {{
          display: block;
          font-size: 12px;
          color: #475569;
          margin-bottom: 6px;
        }}
        .card strong {{
          font-size: 22px;
        }}
        table {{
          width: 100%;
          border-collapse: collapse;
          margin-top: 14px;
        }}
        th, td {{
          border: 1px solid #cbd5e1;
          padding: 8px;
          text-align: left;
          vertical-align: top;
          font-size: 12px;
        }}
        th {{
          background: #1f3864;
          color: white;
        }}
        .section {{
          margin-top: 24px;
        }}
        .insight {{
          border-left: 4px solid #2563eb;
          background: #eff6ff;
          padding: 12px 14px;
        }}
      </style>
    </head>
    <body>
      <div class="header">
        <div class="eyebrow">Execution Intelligence PDF Export</div>
        <h1>{run['xml_filename']}</h1>
        <p>{run['timestamp_raw'] or run['timestamp_display']}</p>
      </div>

      <div class="grid">
        <div class="card"><span>Total cases</span><strong>{run['tests']}</strong></div>
        <div class="card"><span>Passed</span><strong>{run['passed']}</strong></div>
        <div class="card"><span>Failed</span><strong>{run['failures'] + run['errors']}</strong></div>
        <div class="card"><span>Skipped</span><strong>{run['skipped']}</strong></div>
        <div class="card"><span>Pass rate</span><strong>{run['pass_rate']}%</strong></div>
        <div class="card"><span>Total time</span><strong>{format_duration(run['time_seconds'])}</strong></div>
      </div>

      <div class="section">
        <div class="eyebrow">Automated Insights</div>
        <div class="insight">{automated_insights}</div>
      </div>

      <div class="section">
        <div class="eyebrow">Critical Failures</div>
        <h2>Failure list</h2>
        <table>
          <thead>
            <tr>
              <th>Case ID</th>
              <th>Test name</th>
              <th>Severity</th>
              <th>Module</th>
              <th>Error snippet</th>
            </tr>
          </thead>
          <tbody>
            {failures_html}
          </tbody>
        </table>
      </div>
    </body>
    </html>
    """


def generate_pdf_report(run: dict, critical_failures: list[dict], automated_insights: str, output_path: Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_html_path = output_path.with_suffix(".print.html")
    temp_html_path.write_text(
        _build_report_html(run, critical_failures, automated_insights),
        encoding="utf-8",
    )

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1600,1200")
    options.add_argument("--allow-file-access-from-files")
    options.add_argument("--enable-local-file-accesses")

    driver = webdriver.Chrome(service=Service(_get_chromedriver_path()), options=options)
    try:
        driver.get(temp_html_path.resolve().as_uri())
        pdf = driver.execute_cdp_cmd(
            "Page.printToPDF",
            {
                "printBackground": True,
                "paperWidth": 8.27,
                "paperHeight": 11.69,
                "marginTop": 0.4,
                "marginBottom": 0.4,
                "marginLeft": 0.35,
                "marginRight": 0.35,
            },
        )
        output_path.write_bytes(base64.b64decode(pdf["data"]))
    finally:
        driver.quit()
        temp_html_path.unlink(missing_ok=True)

    return output_path
