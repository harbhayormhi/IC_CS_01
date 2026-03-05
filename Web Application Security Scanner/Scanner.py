# scanner.py
import requests

sql_payloads = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "\" OR \"1\"=\"1"
]

def test_sql_injection(url):
    vulnerable = False
    # Use a simple approach: append payload as a query parameter if possible
    for payload in sql_payloads:
        try:
            if "?" in url:
                test_url = url + "&test=" + payload
            else:
                test_url = url + "?" + "test=" + payload

            resp = requests.get(test_url, timeout=10)
            text = resp.text.lower() if resp.text else ""

            errors = ["sql syntax", "mysql", "database error", "unrecognized token"]
            for error in errors:
                if error in text:
                    vulnerable = True
                    break
            if vulnerable:
                break
        except requests.RequestException:
            # skip this payload if the request fails
            continue

    return vulnerable

xss_payload = "<script>alert('XSS')</script>"

def test_xss(url):
    try:
        if "?" in url:
            test_url = url + "&xss=" + xss_payload
        else:
            test_url = url + "?xss=" + xss_payload

        resp = requests.get(test_url, timeout=10)
        if xss_payload in (resp.text or ""):
            return True
    except requests.RequestException:
        pass

    return False
