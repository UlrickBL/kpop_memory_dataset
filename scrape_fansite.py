import os
import time
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://kprofiles.com"
LIST_PAGES = [
    "https://kprofiles.com/k-pop-boy-groups/",
    "https://kprofiles.com/k-pop-girl-groups/"
]

HEADERS = {
    "User-Agent": "KPopEngramBot/1.0"
}

OUT_DIR = "kprofiles_group_data"
os.makedirs(OUT_DIR, exist_ok=True)

def fetch_url(url):
    """Fetch a page, return BeautifulSoup."""
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, "html.parser")

def extract_group_links(soup):
    """From a group list page, find all group profile URLs."""
    container = soup.find("div", class_="entry-content herald-entry-content")
    if not container:
        return []
    
    links = []
    for a in container.find_all("a", href=True):
        href = a["href"]
        if href.endswith("-members-profile/"):
            links.append(href)
    return links

def scrape_group_page(url):
    """
    Scrape a single group profile page.
    Parse <p> tags, grouping paragraphs under <strong> section headings.
    """
    soup = fetch_url(url)

    title_tag = soup.find("h1")
    group_name = title_tag.get_text(strip=True) if title_tag else url

    data = {
        "group": group_name,
        "url": url,
        "sections": []
    }

    paras = soup.find_all("p")
    current_section = None
    buffer = []

    def flush_section():
        """Write buffered paragraphs."""
        if current_section is not None and buffer:
            data["sections"].append({
                "section_title": current_section,
                "content": "\n".join(buffer)
            )

    for p in paras:
        strong_tag = p.find("strong")
        if strong_tag:
            flush_section()
            current_section = strong_tag.get_text(strip=True)
            buffer = []
            strong_tag.extract()

        text = p.get_text(" ", strip=True)
        if text:
            buffer.append(text)

    flush_section()

    return data

def main():
    all_group_data = []

    for list_url in LIST_PAGES:
        print(f"Fetching group list: {list_url}")
        list_soup = fetch_url(list_url)
        group_links = extract_group_links(list_soup)
        
        print(f"Found {len(group_links)} groups on page.")
        for link in group_links:
            full_url = link if link.startswith("http") else BASE_URL + link
            print(f"  Scraping group: {full_url}")

            try:
                group_data = scrape_group_page(full_url)
                all_group_data.append(group_data)
                
                time.sleep(1.5)

            except Exception as e:
                print(f"    Failed on {full_url}: {e}")

    out_path = os.path.join(OUT_DIR, "kprofiles_groups.jsonl")
    with open(out_path, "w", encoding="utf-8") as f:
        for entry in all_group_data:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print("Done. Saved to:", out_path)

if __name__ == "__main__":
    main()
