import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse
import re
import os  

def crawl_and_save(start_url, output_file, max_links=50):
    visited_links = set()  
    to_visit = [start_url]  
    found_links = []  

    while to_visit and len(found_links) < max_links:
        url = to_visit.pop(0)

        if url in visited_links:
            continue

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"URL'e erişilemedi: {url} - Hata: {e}")
            continue

        visited_links.add(url)
        print(f"Ziyaret ediliyor: {url}")

        for link in soup.find_all('a', href=True):
            full_url = urljoin(url, link['href'])  
            if full_url not in visited_links and full_url not in to_visit:
                to_visit.append(full_url)
                found_links.append(full_url)

            if len(found_links) >= max_links:
                break

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(found_links, f, ensure_ascii=False, indent=4)

    print(f"{len(found_links)} bağlantı {output_file} dosyasına kaydedildi.")

user_input = input("URL' GİRİN: ").strip()

if not user_input.startswith("http://") and not user_input.startswith("https://"):
    user_input = "http://" + user_input

start_url = user_input

project_dir = "/Crawler"

parsed_url = urlparse(start_url)
domain_name = re.sub(r'\W+', '_', parsed_url.netloc)  
output_file = os.path.join(project_dir, f"{domain_name}.json")  

crawl_and_save(start_url, output_file)
