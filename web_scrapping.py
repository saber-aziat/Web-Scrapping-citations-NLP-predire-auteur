import os
import csv
import requests
from bs4 import BeautifulSoup
import sys
sys.stdout.reconfigure(encoding='utf-8')

from bs4 import BeautifulSoup
import requests


fichier = "quotes.csv"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# scarpping des 10 pages du site https://quotes.toscrape.com/

print(f"--------------------------------chargement de la site N 1 en cours... --------------------------------")
for NumberOfPage in range(1, 11):

    print(f"Scrapping de la page {NumberOfPage} en cours...")
    url = f"https://quotes.toscrape.com/page/{NumberOfPage}/"
    response = requests.get(url , headers=headers)

    if response.ok:

        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            citation = quote.find("span", class_="text").text.strip()
            author = quote.find("small", class_="author").text
            tags = quote.find_all("a", class_="tag")

            tag = []
            for tagg in tags:
                tag.append(tagg.text)

            page = NumberOfPage

            # Enregistrer les donnes sur le fichier CSV 
            if not os.path.exists(fichier):
                with open(fichier, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Citation", "Author", "Tags", "Page"])
                    writer.writerow([citation, author, ", ".join(tag), page])
            else:
                with open(fichier, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([citation, author, ", ".join(tag), page])

    else:
        print(f"Erreur sur la page {NumberOfPage}: {response.status_code}")

# scarpping des 100 pages du site https://www.goodreads.com/quotes
print("=" * 50)
print(f"--------------------------------chargement de la site N 2 en cours... --------------------------------")

for NumberOfPage in range(1,101):
    print(f"Scrapping de la page {NumberOfPage} en cours...")
    url = f"https://www.goodreads.com/quotes?page={NumberOfPage}"
    response = requests.get(url, headers=headers)

    if response.ok:
         soup = BeautifulSoup(response.text, 'lxml')
         quotes = soup.find_all("div", class_="quote")

         for quote in quotes:

            # Citation
            citation_div = quote.find("div", class_="quoteText")
            citation = citation_div.text.split("―")[0].strip().replace('“','').replace('”','')

            # Author
            author_span = quote.find("span", class_="authorOrTitle")
            author = author_span.text.strip()

            # Tags
            tags_div = quote.find("div", class_="greyText smallText left")
            tags = []
            if tags_div is not None:
                tagss = tags_div.find_all("a")
                for tag in tagss:
                    tags.append(tag.text.strip())

            # Enregistrer dans CSV
            if not os.path.exists(fichier):
                with open(fichier, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Citation", "Author", "Tags", "Page"])
                    writer.writerow([citation, author, ", ".join(tags), NumberOfPage])
            else:
                with open(fichier, "a", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow([citation, author, ", ".join(tags), NumberOfPage])

    else:
       print(f"Erreur sur la page {NumberOfPage}: {response.status_code}")



  


        
