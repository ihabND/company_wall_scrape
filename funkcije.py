import json
from time import sleep
from bs4 import BeautifulSoup
import requests
from util import *
from util import filtrirajTekst

def to_md(firme):
    md = []

    for c in firme:
        md.append(f"## {c['ime']}")
        md.append("")
        md.append(f"**PIB:** {c['pib']}")
        md.append("")
        md.append(f"**MIB:** {c['mib']}")
        md.append("")
        md.append(f"**Datum osnivanja:** {c['datum_osnivanja']}")
        md.append("")
        md.append(f"**Šifra delatnosti:** {c['sifra_delatnosti']}")
        md.append("")
        md.append(f"**Veličina preduzeća:** {c['velicina_preduzeca']}")
        md.append("")
        md.append(f"**Adresa:** {c['adresa']}")
        md.append("")

        if c.get("telefon"):
            md.append("**Telefoni:**")
            for tel in c["telefon"]:
                md.append(f"- {tel}")
            md.append("")

        if c.get("email"):
            md.append("**Email:**")
            for email in c["email"]:
                md.append(f"- {email}")
            md.append("")

        md.append("---")
        md.append("")

    return "\n".join(md)

def get_company_links():
    response = requests.get(URL, proxies=proxies, headers=headers, timeout=60)
    page = BeautifulSoup(response.text, "html.parser")

    firme = page.find(id="tabContent")
    links = firme.find_all("a", href=True)
    firme_linkovi = [link for link in links if link["href"].startswith("/firma/")]

    return firme_linkovi


def get_company_data(link):
    link = BASE + str(link["href"])
    sleep(0.3)

    response_individualna = requests.get(
        link,
        proxies=proxies,
        headers=headers,
        timeout=60
    )

    individualna_stranica = BeautifulSoup(
        response_individualna.text,
        "html.parser"
    )

    ime = individualna_stranica.select_one('[itemprop="name"]').text
    pib = individualna_stranica.select_one('[itemprop="vatID"]').text

    ulica = individualna_stranica.select_one('[itemprop="streetAddress"]').text
    postanski = individualna_stranica.select_one('[itemprop="postalCode"]').text
    grad = individualna_stranica.select_one('[itemprop="addressLocality"]').text

    adresa = [ulica, postanski, grad]
    adresa = ", ".join(adresa)

    # paragraphs = individualna_stranica.select(
    #     "section.panel.align-self-stretch p"
    # )

    # opis = " ".join(p.get_text(strip=True) for p in paragraphs)

    kontakt_div = individualna_stranica.find("div", class_="contact-summary")
    kontakt = kontakt_div.find_all("span")
    kontakti = []
    for podatak in kontakt:
        kontakti.append(podatak.text)
    telefon = []
    email = []
    for kontakt in kontakti:
        if "@" in kontakt:
            email.append(kontakt)
        else:
            telefon.append(kontakt)
        
    info = []
    firma_podaci_div = individualna_stranica.find("div", class_="business-info")
    firma_podaci = firma_podaci_div.find_all()
    for podatak in firma_podaci:
        info.append(podatak.text)
    mib = info[20]
    datum = info[22]
    delatnost = info[24]
    velicina = info[26]

    firma = {}
    firma["ime"] = ime
    firma["pib"] = pib
    firma["mib"] = mib
    firma["datum_osnivanja"] = datum
    delatnost = filtrirajTekst(delatnost)
    firma["sifra_delatnosti"] = delatnost
    firma["adresa"] = adresa
    firma["velicina_preduzeca"] = velicina
    firma["telefon"] = telefon
    firma["email"] = email

    # firma["opis"] = opis

    return firma


def save_files(firme_lista):
    mdLista = to_md(firme_lista)

    with open("firme.md", "w", encoding="utf-8") as file:
        file.write(mdLista)

    with open("firme.txt", "w", encoding="utf-16") as file:
        json.dump(firme_lista, file, indent=2)