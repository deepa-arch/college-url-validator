import socket
import requests
import urllib3
import re
from urllib.parse import urlparse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Utility Functions
# -----------------------------

def normalize_domain(input_url: str) -> str:
    input_url = input_url.strip().lower()

    if not input_url.startswith(("http://", "https://")):
        input_url = "https://" + input_url

    parsed = urlparse(input_url)

    domain = parsed.hostname

    if domain and domain.startswith("www."):
        domain = domain[4:]

    return domain


def clean_text(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9 ]', '', text).lower()


def fetch_website_title(domain: str):
    urls_to_try = [
        f"https://{domain}",
        f"https://www.{domain}",
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }

    for url in urls_to_try:
        try:
            response = requests.get(
                url,
                timeout=5,
                headers=headers,
                allow_redirects=True,
                verify=False
            )

            if response.status_code < 500:
                soup = BeautifulSoup(response.text, "html.parser")

                if soup.title and soup.title.string:
                    return url, soup.title.string.strip()

                return url, None

        except requests.exceptions.RequestException:
            continue

    return None, None


# -----------------------------
# Main Endpoint
# -----------------------------

@app.get("/validate")
def validate_domain(college_name: str, domain: str):

    result = {
        "isValid": False,
        "workingURL": None,
        "title": None,
        "similarity_score": 0,
        "checks": {
            "format": False,
            "dns": False,
            "name_match": False
        },
        "warnings": [],
        "errors": []
    }

    # Normalize domain
    domain = normalize_domain(domain)

    # 1️⃣ Format Check
    if not domain or "." not in domain:
        result["errors"].append("Invalid domain format")
        return result

    result["checks"]["format"] = True

    # 2️⃣ DNS Check
    try:
        socket.gethostbyname(domain)
        result["checks"]["dns"] = True
        result["isValid"] = True
    except socket.gaierror:
        result["errors"].append("Domain does not exist")
        return result

    # 3️⃣ Fetch Title
    working_url, title = fetch_website_title(domain)

    result["workingURL"] = working_url
    result["title"] = title

    if title:
        college_clean = clean_text(college_name)
        title_clean = clean_text(title)

        similarity = fuzz.token_set_ratio(college_clean, title_clean)

        result["similarity_score"] = similarity

        if similarity >= 60:   # Threshold
            result["checks"]["name_match"] = True
        else:
            result["warnings"].append(
                "Domain exists but title does not strongly match college name"
            )
    else:
        result["warnings"].append(
            "Could not extract website title"
        )

    return result
