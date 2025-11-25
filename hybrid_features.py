import requests
import tldextract
from bs4 import BeautifulSoup

def extract_features(url):
    feats = {}

    feats["url_length"] = len(url)
    feats["has_https"] = int(url.startswith("https"))
    feats["num_digits"] = sum(c.isdigit() for c in url)
    feats["num_special_chars"] = sum(not c.isalnum() for c in url)
    feats["num_subdomains"] = url.count(".") - 1

    SUSPICIOUS = ["login", "verify", "update", "password", "bank", "crypto", "secure"]
    feats["keyword_score"] = sum(k in url.lower() for k in SUSPICIOUS)

    ext = tldextract.extract(url)
    feats["tld_length"] = len(ext.suffix)

    try:
        r = requests.get(url, timeout=4, allow_redirects=True)
        feats["status"] = r.status_code
        feats["redirects"] = len(r.history)

        soup = BeautifulSoup(r.text, "html.parser")
        feats["forms"] = len(soup.find_all("form"))
        feats["password_fields"] = int(bool(soup.find("input", {"type": "password"})))
        feats["scripts"] = len(soup.find_all("script"))
        feats["iframes"] = len(soup.find_all("iframe"))
    except:
        feats.update({
            "status": 0, "redirects": 0, "forms": 0,
            "password_fields": 0, "scripts": 0, "iframes": 0
        })

    return feats
