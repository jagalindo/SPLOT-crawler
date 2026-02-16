"""Tests for the configuration module."""

from pathlib import Path

from config import (
    BASE_DIR,
    FAMA_XML_DIR,
    SPLOT_BASE_URL,
    SPLOT_CATALOGUE_URL,
    SPLOT_MODELS_URL,
    SPLOT_XML_DIR,
    SPLX_TO_FAMA_JAR,
    UVL_DIR,
)


def test_base_dir_is_project_root():
    assert BASE_DIR.is_dir()
    assert (BASE_DIR / "config.py").exists()


def test_splot_urls_are_well_formed():
    assert SPLOT_BASE_URL.startswith("http://")
    assert "SPLOT" in SPLOT_BASE_URL
    assert SPLOT_MODELS_URL.startswith(SPLOT_BASE_URL)
    assert SPLOT_CATALOGUE_URL.startswith(SPLOT_BASE_URL)
    assert "action=select_model" in SPLOT_CATALOGUE_URL


def test_directories_are_path_objects():
    assert isinstance(SPLOT_XML_DIR, Path)
    assert isinstance(FAMA_XML_DIR, Path)
    assert isinstance(UVL_DIR, Path)


def test_conversion_tools_paths():
    assert isinstance(SPLX_TO_FAMA_JAR, Path)
    assert SPLX_TO_FAMA_JAR.name == "splx_to_fama.jar"
