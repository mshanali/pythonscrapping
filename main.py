import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse, urljoin

def scrape_and_count(url, keyword):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    lines = soup.find_all(string=re.compile(rf'{keyword}', re.IGNORECASE))
    return lines

def count_occurrences(lines):
    return len(lines)

def print_links(links):
    if len(links) > 0:
        print("Link where the keyword appears:")
        for link in links:
            print(link)
    else:
        print("No links found.")

def scrape_website(url, keywords):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all('a', href=True)
    base_url = urlparse(url).scheme + "://" + urlparse(url).netloc
    pages = []

    for link in links:
        page_url = urljoin(base_url, link['href'])
        if page_url not in pages and page_url.rstrip('/') != base_url.rstrip('/'):
            pages.append(page_url)

    lines = []
    keyword_counts = {keyword: 0 for keyword in keywords}
    keyword_links = {keyword: [] for keyword in keywords}

    for page in pages:
        page_lines = scrape_and_count(page, keywords)
        lines.extend(page_lines)

        for i, line in enumerate(page_lines, start=1):
            line_text = line.strip()
            for keyword in keywords:
                if keyword.lower() in line_text.lower():
                    keyword_counts[keyword] += 1
                    keyword_links[keyword].append(page)

    print("Occurrences of keywords:")
    for keyword, count in keyword_counts.items():
        print(f"Total occurrences of '{keyword}': {count}")
    print()
    for keyword, links in keyword_links.items():
        print(f"Links where the keyword '{keyword}' appears:")
        for link in links:
            print(link)
        print()

url = input("Enter the website URL: ")
num_keywords = int(input("Enter the number of keywords you want to scrape: "))

keywords = []
for i in range(1, num_keywords + 1):
    keyword = input(f"Enter keyword {i}: ")
    keywords.append(keyword)

scrape_website(url, keywords)
