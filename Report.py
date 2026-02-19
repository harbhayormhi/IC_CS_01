# report.py
def generate_report(results):
    print("\n===== SCAN REPORT =====")

    for result in results:
        print(f"\nURL: {result.get('url')}")
        print(f"SQL Injection: {result.get('sql')}")
        print(f"XSS: {result.get('xss')}")
        headers = result.get('headers')
        print(f"Missing Headers: {headers}")
