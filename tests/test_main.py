from typing import Any
from unittest.mock import MagicMock, patch


from main import main

class TestMain:
    """
    Tests for the main function of the CLI tool.
    """
    @patch("main.ReportFactory")
    @patch("main.read_csv_files")
    def test_main_success(self, mock_read_csv: Any, mock_factory: Any) -> None:
        """
        Tests successful execution of the main script with valid inputs.
        """
        mock_read_csv.return_value = [{"country": "USA", "year": "2023", "gdp": "25000"}]

        mock_report_instance = MagicMock()
        mock_report_instance.generate.return_value = {
            "headers": ["Country", "Average GDP"],
            "rows": [["USA", "25000.0"]],
        }
        mock_factory.get_report.return_value = mock_report_instance
        mock_factory.get_available_reports.return_value = ["average-gdp"]

        with patch(
            "sys.argv",
            ["main.py", "--files", "test.csv", "--report", "average-gdp"],
        ):
            with patch("sys.exit") as mock_exit:
                main()
                mock_exit.assert_not_called()

        mock_read_csv.assert_called_with(["test.csv"])
        mock_factory.get_report.assert_called_with("average-gdp")
        mock_report_instance.generate.assert_called_once()