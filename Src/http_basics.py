
import requests
import json
from datetime import datetime, timezone
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Target application
url = "http://127.0.0.1:3000"

# Report data
report = {
    "project": "Automated Web Application Security Assessment for Financial Platforms",
    "task": "Week 2 - Python for Security and HTTP Fundamentals",
    "target": url,
    "scan_time_utc": datetime.now(timezone.utc).isoformat(),
    "method": "GET",
    "status": "failed",
    "http_status_code": None,
    "response_headers": {},
    "content_type": None,
    "server_header": None,
    "response_size_bytes": None,
    "response_preview": None,
    "error": None
}

try:
    response = requests.get(url, timeout=10)

    report.update({
        "status": "completed",
        "http_status_code": response.status_code,
        "response_headers": dict(response.headers),
        "content_type": response.headers.get("Content-Type"),
        "server_header": response.headers.get("Server"),
        "response_size_bytes": len(response.content),
        "response_preview": response.text[:300]
    })

    print("Target URL:", url)
    print("Status Code:", response.status_code)
    print("Content Type:", response.headers.get("Content-Type"))
    print("Server Header:", response.headers.get("Server"))
    print("Response Size:", len(response.content), "bytes")

except requests.exceptions.RequestException as error:
    report["error"] = str(error)
    print("Request failed:", error)

# Save the report
report_path = REPORTS_DIR / "week2_http_report.json"

with report_path.open("w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("\nReport saved to:")
print(report_path)
