"""Tests for the statistics module."""

import importlib.util
import sys
from unittest.mock import MagicMock, patch

spec = importlib.util.spec_from_file_location("get_statistics", "4.get_statistics.py")
statistics = importlib.util.module_from_spec(spec)
sys.modules["get_statistics"] = statistics
spec.loader.exec_module(statistics)


SAMPLE_TABLE_HTML = """
<html><body>
<table>
<tr><th>Model #</th><th>Name</th><th>Features</th></tr>
<tr><td>1</td><td>ModelA</td><td>10</td></tr>
<tr><td>2</td><td>ModelB</td><td>25</td></tr>
</table>
</body></html>
"""


@patch("get_statistics.requests.get")
def test_fetch_statistics_parses_table(mock_get):
    mock_response = MagicMock()
    mock_response.content = SAMPLE_TABLE_HTML.encode()
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    result = statistics.fetch_statistics()

    assert len(result) == 2
    assert result[0]["Name"] == "ModelA"
    assert result[1]["Features"] == "25"


def test_save_statistics_creates_files(tmp_path):
    stats_file = tmp_path / "statistics.json"
    readme_file = tmp_path / "README.md"
    readme_file.write_text("# Header\n")

    table_data = [{"Name": "Test", "Features": "5"}]

    with patch("get_statistics.STATISTICS_FILE", stats_file), \
         patch("get_statistics.README_FILE", readme_file):
        statistics.save_statistics(table_data)

    assert stats_file.exists()
    assert "Test" in stats_file.read_text()
    assert "Model Statistics" in readme_file.read_text()
