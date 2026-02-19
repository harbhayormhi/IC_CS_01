# crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

visited_links = set()

def is_same_domain(base, link):
    return urlparse(base).netloc == urlparse(link).netloc

def crawl(url, max_depth=2, current_depth=0):
    if current_depth > max_depth:
        return []

    links = []

    try:
        # Timeout and simple retry loop (no external lib)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup.find_all("a", href=True):
            link = urljoin(url, tag["href"])
            # Normalize to remove fragments
            link = link.split("#")[0]

            if link not in visited_links and is_same_domain(url, link):
                visited_links.add(link)
                links.append(link)

        return links

    except requests.RequestException as e:
        # Log the error in real usage
        # print(f" crawl error for {url}: {e}")
        return []
