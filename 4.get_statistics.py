"""Extract model metadata from SPLOT and generate statistics."""

import json
import logging

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

from config import (
    README_FILE,
    REQUEST_TIMEOUT_SECONDS,
    SPLOT_CATALOGUE_URL,
    STATISTICS_FILE,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def fetch_statistics():
    """Fetch model statistics table from the SPLOT catalogue page."""
    logger.info("Fetching statistics from %s", SPLOT_CATALOGUE_URL)
    response = requests.get(SPLOT_CATALOGUE_URL, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    headers = [header.text for header in soup.find_all("th")]

    table_data = []
    for row in soup.find_all("tr"):
        columns = row.find_all("td")
        output_row = {}
        for header, column in zip(headers, columns):
            if column.find("a"):
                output_row[header] = column.find("a")["href"].split("=")[-1]
            else:
                output_row[header] = column.text.strip()
        if output_row:
            table_data.append(output_row)

    logger.info("Extracted metadata for %d models", len(table_data))
    return table_data


def save_statistics(table_data):
    """Save statistics as JSON and append a markdown table to the README."""
    with open(STATISTICS_FILE, "w") as f:
        json.dump(table_data, f, indent=4)
    logger.info("Saved statistics to %s", STATISTICS_FILE)

    markdown_table = tabulate(table_data, headers="keys", tablefmt="pipe")
    with open(README_FILE, "a") as f:
        f.write("\n## Model Statistics\n\n")
        f.write("Below, you can find the current statistics of the models from SPLOT\n\n")
        f.write(markdown_table)
        f.write("\n")
    logger.info("Appended statistics table to %s", README_FILE)


def main():
    table_data = fetch_statistics()
    save_statistics(table_data)


if __name__ == "__main__":
    main()
