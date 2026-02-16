"""Centralized configuration for the SPLOT crawler pipeline."""

import os
from pathlib import Path

# Base directory (project root)
BASE_DIR = Path(__file__).resolve().parent

# SPLOT server configuration
SPLOT_HOST = os.environ.get("SPLOT_HOST", "52.32.1.180")
SPLOT_PORT = os.environ.get("SPLOT_PORT", "8080")
SPLOT_BASE_URL = f"http://{SPLOT_HOST}:{SPLOT_PORT}/SPLOT"
SPLOT_MODELS_URL = f"{SPLOT_BASE_URL}/models"
SPLOT_CATALOGUE_URL = (
    f"{SPLOT_BASE_URL}/SplotAnalysesServlet"
    "?action=select_model&enableSelection=false&&showModelDetails=true"
)

# Directory paths
SPLOT_XML_DIR = BASE_DIR / "splot-xml"
FAMA_XML_DIR = BASE_DIR / "fama-xml"
UVL_DIR = BASE_DIR / "flama-uvl"

# Conversion tools
SPLX_TO_FAMA_JAR = BASE_DIR / "file_conversions" / "splx_to_fama.jar"
FAMA_TO_UVL_SCRIPT = BASE_DIR / "file_conversions" / "fama_to_uvl.py"

# Output files
README_FILE = BASE_DIR / "README.md"
STATISTICS_FILE = BASE_DIR / "statistics.json"

# Download settings
DOWNLOAD_DELAY_SECONDS = int(os.environ.get("DOWNLOAD_DELAY", "10"))
REQUEST_TIMEOUT_SECONDS = int(os.environ.get("REQUEST_TIMEOUT", "30"))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "3"))
