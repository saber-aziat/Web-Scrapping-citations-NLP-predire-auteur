import os
import csv
import requests
from bs4 import BeautifulSoup

fichier = "quotes.csv"

for NumberOfPage in range(1, 11):

    print(f"Scrapping de la page {NumberOfPage} en cours...")
    url = f"https://quotes.toscrape.com/page/{NumberOfPage}/"
    response = requests.get(url)

    if response.ok:

        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            citation = quote.find("span", class_="text").text
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
