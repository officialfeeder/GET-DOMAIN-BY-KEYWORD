import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def get_links_from_search(keyword):
    url = "https://searx.baczek.me/search"
    headers = {
        "authority": "searx.baczek.me",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "null",
        "sec-ch-ua": '^"Not/A)Brand^";v="99", ^"Google Chrome^";v="115", ^"Chromium^";v="115"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '^"Windows^"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    data = {
        "q": keyword,
        "category_general": "1",
        "language": "all",
        "time_range": "",
        "safesearch": "0",
        "theme": "simple"
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()

        # Parsing HTML dengan BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Mencari semua elemen anchor (<a>) dan mengambil tautan (href)
        anchor_links = [a["href"] for a in soup.find_all("a", href=True)]

        return anchor_links

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    filename = input("Masukkan nama file yang berisi kata kunci: ")

    try:
        with open(filename, "r", encoding="utf-8") as file:
            keywords = file.readlines()
            keywords = [keyword.strip() for keyword in keywords]

        output_filename = "search_results.txt"
        unique_links = set()

        with open(output_filename, "w", encoding="utf-8") as output_file:
            for keyword in keywords:
                print(f"===== Keyword: {keyword} =====")
                links = get_links_from_search(keyword)

                for link in links:
                    parsed_url = urlparse(link)
                    domain = parsed_url.netloc.lower()

                    if domain not in unique_links:
                        unique_links.add(domain)
                        output_file.write(link + "\n")

    except FileNotFoundError:
        print(f"File '{filename}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
