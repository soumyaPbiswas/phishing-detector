import joblib
import tldextract
import socket
import pandas as pd

feature_cols = joblib.load("features.pkl")

def extract_features(url):
    ext = tldextract.extract(url)
    domain = ext.registered_domain

    feats = {
        "urllength": len(url),
        "domainlength": len(domain),
        "isdomainip": int(is_ip(domain)),
        "ishttps": int(url.startswith("https")),
        "noofsubdomain": url.count(".") - 1,
        "noofdegitsinurl": sum(c.isdigit() for c in url),
        "noofequalsinurl": url.count("="),
        "noofqmarkinurl": url.count("?"),
        "noofampersandinurl": url.count("&"),
        "noofotherspecialcharsinurl": sum(not c.isalnum() for c in url),
        "spacialcharratioinurl": sum(not c.isalnum() for c in url) / len(url)
    }

    return pd.DataFrame([[feats[col] for col in feature_cols]], columns=feature_cols)

def is_ip(domain):
    import socket
    try:
        socket.inet_aton(domain)
        return True
    except:
        return False
