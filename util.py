import re

PROXY_URL = "http://USERNAME:PASSWORD@PROXY_HOST:PORT"

BASE = "https://www.companywall.rs"
URL = "https://www.companywall.rs/pretraga?cr=RSD&n=&mv=&r=103&c=176&cp=&at=&area=1884&subarea=-1&sbjact=t&blckd=&dbf=&dbt=&type=&hr=&bly=2024&dsm%5B0%5D.Code=1101&dsm%5B0%5D.From=0&dsm%5B0%5D.To=0&dsm%5B1%5D.Code=966&dsm%5B1%5D.From=0&dsm%5B1%5D.To=0&dsm%5B-1%5D.Code=0&dsm%5B-1%5D.From=0&dsm%5B-1%5D.To=0&distinctcodes=&xpnd=true"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    ),
    "Accept-Language": "sr-RS,sr;q=0.9,en;q=0.8"
}

proxies = {
    "http": PROXY_URL,
    "https": PROXY_URL
}

def filtrirajTekst(tekst):
    tekst = re.sub(r"\s+", " ", tekst).strip()
    tekst = re.sub(r"\s*-\s*", ", ", tekst)
    return tekst