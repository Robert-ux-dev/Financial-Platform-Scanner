
import json
from datetime import datetime, timezone
from pathlib import Path

import requests

TARGET_URL = "http://127.0.0.1:3000"
TIMEOUT = 10

REPORT_PATH = (
    Path(__file__).resolve().parent.parent
    / "reports"
    / "week2_http_report.json"
)

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]


def inspect_http_response(response):
    """Collect basic HTTP response and security information."""

    headers = dict(response.headers)

    security_headers = {
        name: headers.get(name)
        for name in SECURITY_HEADERS
    }

    cookies = []
    for cookie in response.cookies:
        cookies.append({
            "name": cookie.name,
            "secure": cookie.secure,
            "httponly": cookie.has_nonstandard_attr("HttpOnly")
            or "httponly" in cookie._rest,
            "samesite": cookie._rest.get("SameSite"),
        })

    return {
        "requested_url": TARGET_URL,
        "final_url": response.url,
        "method": response.request.method,
        "status_code": response.status_code,
        "reason": response.reason,
        "content_type": headers.get("Content-Type"),
        "server_header": headers.get("Server"),
        "response_headers": headers,
        "security_headers": security_headers,
        "cookies_received": cookies,
        "response_size_bytes": len(response.content),
    }


def main():
    report = {
        "project": (
            "Automated Web Application Security Assessment "
            "for Financial Platforms"
        ),
        "scan_time_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "target": TARGET_URL,
        "scope": "Local lab; GET request only",
        "observations": [],
    }

    try:
        response = requests.get(
            TARGET_URL,
            timeout=TIMEOUT,
            allow_redirects=True,
        )

        report["observations"].append(
            inspect_http_response(response)
        )

        print("HTTP request completed.")
        print("Method:", response.request.method)
        print("Status code:", response.status_code)
        print("Final URL:", response.url)
        print("Content-Type:", response.headers.get("Content-Type"))

        print("\nSecurity response headers:")
        for name, value in report["observations"][0][
            "security_headers"
        ].items():
            print(f"{name}: {value or 'Not present'}")

    except requests.RequestException as error:
        report["error"] = str(error)
        print("HTTP request failed:", error)

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(report, indent=4),
        encoding="utf-8",
    )

    print("\nReport saved to:", REPORT_PATH)


if __name__ == "__main__":
    main()
