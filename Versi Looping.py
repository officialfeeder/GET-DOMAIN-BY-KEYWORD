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

        # Menghitung jumlah hasil yang ditemukan
        result_count = len(anchor_links)

        # Mengambil domain dari setiap URL dan menghindari duplikasi
        unique_domains = set(urlparse(link).netloc.lower() for link in anchor_links)

        return unique_domains, result_count

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return set(), 0

if __name__ == "__main__":
    filename = input("Masukkan nama file yang berisi kata kunci: ")
    search_retries = int(input("Jumlah pencarian ulang: "))

    try:
        with open(filename, "r", encoding="utf-8") as file:
            keywords = file.readlines()
            keywords = [keyword.strip() for keyword in keywords]

        output_filename = "search_results.txt"

        # Membuat set kosong untuk menyimpan domain unik
        unique_domains_set = set()

        with open(output_filename, "a", encoding="utf-8") as output_file:  # Gunakan mode "a" untuk append
            for keyword in keywords:
                print(f"===== Keyword: {keyword} =====")
                for _ in range(search_retries):
                    domains, result_count = get_links_from_search(keyword)

                    for domain in domains:
                        # Menambahkan domain ke set domain unik
                        unique_domains_set.add(domain)
                        
                    print(f"Jumlah hasil untuk '{keyword}': {result_count}")

            # Menulis domain-domain unik ke file output
            for unique_domain in unique_domains_set:
                output_file.write(unique_domain + "\n")

    except FileNotFoundError:
        print(f"File '{filename}' tidak ditemukan.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
