"""Download feature models from the SPLOT repository."""

import logging
import time
import urllib.request
from urllib.parse import parse_qs, urlparse

import requests
from bs4 import BeautifulSoup

from config import (
    DOWNLOAD_DELAY_SECONDS,
    MAX_RETRIES,
    REQUEST_TIMEOUT_SECONDS,
    SPLOT_CATALOGUE_URL,
    SPLOT_MODELS_URL,
    SPLOT_XML_DIR,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def fetch_model_links():
    """Fetch the list of model download links from the SPLOT catalogue."""
    logger.info("Fetching model catalogue from %s", SPLOT_CATALOGUE_URL)
    response = requests.get(SPLOT_CATALOGUE_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    model_names = []

    for tag in soup.find_all("a"):
        href = tag.get("href", "")
        if "modelFile" not in href:
            continue
        query = urlparse(href).query
        params = parse_qs(query)
        names = params.get("modelFile", [])
        if names and names[0].endswith(".xml"):
            model_names.append(names[0])

    logger.info("Found %d XML models in catalogue", len(model_names))
    return model_names


def download_model(model_name):
    """Download a single model file with retry logic."""
    dest = SPLOT_XML_DIR / model_name
    if dest.exists():
        return False

    download_url = f"{SPLOT_MODELS_URL}/{model_name}"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.info("Downloading %s (attempt %d/%d)", model_name, attempt, MAX_RETRIES)
            urllib.request.urlretrieve(download_url, str(dest))
            return True
        except Exception as exc:
            logger.warning("Failed to download %s: %s", model_name, exc)
            if attempt < MAX_RETRIES:
                wait = 2 ** attempt
                logger.info("Retrying in %ds...", wait)
                time.sleep(wait)
            else:
                logger.error("Giving up on %s after %d attempts", model_name, MAX_RETRIES)
                if dest.exists():
                    dest.unlink()
                return False


def main():
    SPLOT_XML_DIR.mkdir(parents=True, exist_ok=True)

    model_names = fetch_model_links()
    downloaded = 0
    skipped = 0

    for model_name in model_names:
        if download_model(model_name):
            downloaded += 1
            time.sleep(DOWNLOAD_DELAY_SECONDS)
        else:
            skipped += 1

    logger.info(
        "Done. Downloaded: %d, Skipped (already present or failed): %d",
        downloaded,
        skipped,
    )


if __name__ == "__main__":
    main()
