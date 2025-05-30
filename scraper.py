import requests
from bs4 import BeautifulSoup

def get_homepage_text(url):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        texts = soup.stripped_strings
        return " ".join(texts)[:5000]  # Limit text size
    except:
        return ""
