import bs4 
import requests
import webbrowser as wb 
from pprint import pprint
import csv


nuovo = input("Nuovo? [s/n]  ")

if nuovo == "s":
    regione = input("Regione? ")
    categoria = input("Categoria? ")
    ricerca = input("Ricerca? ")
    nomeRicerca = input("nome ricerca? ")
    # metti tutto in "./offerte_subito.it/controllati.csv"
    with open("./offerte_subito.it/controllati.csv", "w") as filecsv:
        scrivi = csv.writer(filecsv, delimiter=',')
        scrivi.writerow([nomeRicerca, regione, categoria, ricerca])
elif nuovo == "n":
    print("scegli tra:")
    # stampa contenuto file controllati.csv
    with open("./offerte_subito.it/controllati.csv", "r") as filecsv:
        lettore = csv.reader(filecsv, delimiter=',')
        for row in lettore:
            print(row[0])
    nomeRicerca = input("nomeRicerca? ")
    # prendi i valori da "./offerte_subito.it/controllati.csv"
    with open("./offerte_subito.it/controllati.csv", "r") as filecsv:
        lettore = csv.reader(filecsv, delimiter=',')
        for row in lettore:
            if row[0] == nomeRicerca:
                regione = row[1]
                categoria = row[2]
                ricerca = row[3]

ricerca = ricerca.replace(' ', '%20')
link = "https://www.subito.it/annunci-" + regione + "/vendita/" + categoria + "/?q=" + ricerca
pre_link_annuncio = "https://www.subito.it/" + categoria

res = requests.get(link)
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "html.parser")
div_annunci = soup.find("div", class_ = "jsx-1413137898 col items")

a_annunci = div_annunci.find_all('a')   # trova tutti gli <a> presenti nel div annunci
link_annunci = []
for a_annuncio in a_annunci:
    link_annuncio = str(a_annuncio.get("href"))
    if pre_link_annuncio in link_annuncio:
        link_annunci.append(link_annuncio)

f = open("./offerte_subito.it/" + nomeRicerca + ".txt", "a")
old_link_annunci = [riga.rstrip('\n') for riga in open("./offerte_subito.it/" + nomeRicerca + ".txt")]
new_link_annuni = []
for link_annuncio in link_annunci:
    if link_annuncio not in old_link_annunci:
        new_link_annuni.append(link_annuncio)
        f.write('%s\n' % link_annuncio)
f.close()
if new_link_annuni:
    print("nuovi risultati, apertura in corso...")
    for new_link in new_link_annuni:
        wb.open(new_link)
else:
    print("nessun nuovo annuncio :( ")

input("...")