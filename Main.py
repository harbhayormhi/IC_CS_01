# main.py
from crawler import crawl
from scanner import test_sql_injection, test_xss
from headers import check_headers
from report import generate_report

def main():
    target = input("Enter Target URL: ").strip()
    if not target:
        print("No URL provided.")
        return

    links = crawl(target)
    # If crawl returns no links, still test the target itself
    if not links:
        links = [target]

    results = []

    for link in links:
        print("Scanning:", link)

        result = {
            "url": link,
            "sql": test_sql_injection(link),
            "xss": test_xss(link),
            "headers": check_headers(link)
        }

        results.append(result)

    generate_report(results)

if _name_=="_main_":
    main()
