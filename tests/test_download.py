"""Tests for the download module."""

import importlib.util
import sys
from unittest.mock import MagicMock, patch

spec = importlib.util.spec_from_file_location("download", "1.download.py")
download = importlib.util.module_from_spec(spec)
sys.modules["download"] = download
spec.loader.exec_module(download)


SAMPLE_HTML = """
<html><body>
<table>
<tr><td><a href="/SPLOT/SplotAnalysesServlet?action=download&modelFile=model1.xml">model1</a></td></tr>
<tr><td><a href="/SPLOT/SplotAnalysesServlet?action=download&modelFile=model2.xml">model2</a></td></tr>
<tr><td><a href="/SPLOT/SplotAnalysesServlet?action=download&modelFile=model3.sxfm">model3</a></td></tr>
<tr><td><a href="/other/link">no model</a></td></tr>
</table>
</body></html>
"""


@patch("download.requests.get")
def test_fetch_model_links_parses_xml_models(mock_get):
    mock_response = MagicMock()
    mock_response.text = SAMPLE_HTML
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    result = download.fetch_model_links()

    assert "model1.xml" in result
    assert "model2.xml" in result
    # .sxfm files should be excluded
    assert "model3.sxfm" not in result
    assert len(result) == 2


@patch("download.urllib.request.urlretrieve")
def test_download_model_skips_existing(mock_urlretrieve, tmp_path):
    existing_file = tmp_path / "existing.xml"
    existing_file.touch()

    with patch("download.SPLOT_XML_DIR", tmp_path):
        result = download.download_model("existing.xml")

    assert result is False
    mock_urlretrieve.assert_not_called()


@patch("download.urllib.request.urlretrieve")
def test_download_model_downloads_new(mock_urlretrieve, tmp_path):
    with patch("download.SPLOT_XML_DIR", tmp_path):
        result = download.download_model("new_model.xml")

    assert result is True
    mock_urlretrieve.assert_called_once()
