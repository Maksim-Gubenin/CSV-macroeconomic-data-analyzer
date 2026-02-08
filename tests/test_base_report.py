import logging
from io import StringIO
from unittest.mock import patch

import pytest

from reports.base_report import BaseReport


class TestBaseReport:
    """
    Tests for the abstract base class BaseReport and its core functionality.
    """
    def test_abstract_method_raises_error(self) -> None:
        """
        Ensures that an abstract base class cannot be instantiated directly.
        """
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            BaseReport()  # type: ignore

    def test_concrete_class_must_implement_generate(self) -> None:
        """
        Ensures that a concrete subclass must implement the 'generate' method.
        """
        class InvalidReport(BaseReport):  # type: ignore
            pass

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            InvalidReport()  # type: ignore

    def test_valid_concrete_class(self) -> None:
        """
        Ensures a properly implemented subclass can be instantiated and has required methods.
        """
        class ValidReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {"headers": [], "rows": []}

        report = ValidReport()
        assert hasattr(report, "generate")
        assert hasattr(report, "print_report")

    def test_print_report_empty_data(self, caplog) -> None:
        """
        Tests that logging is used correctly when the report data is empty.
        """
        class TestReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {}

        report = TestReport()

        with caplog.at_level(logging.INFO):
            report.print_report({})
            assert "Нет данных для отображения" in caplog.text

    def test_print_report_valid_data(self) -> None:
        """
        Tests that tabulate is called correctly with valid report data.
        """
        class TestReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {}

        report = TestReport()
        test_result = {
            "headers": ["Country", "GDP"],
            "rows": [["USA", "25000"], ["China", "18000"]],
        }

        with patch("sys.stdout", new_callable=StringIO):
            with patch("reports.base_report.tabulate") as mock_tabulate:
                report.print_report(test_result)
                mock_tabulate.assert_called_once_with(
                    [["USA", "25000"], ["China", "18000"]],
                    headers=["Country", "GDP"],
                    tablefmt="grid",
                    stralign="center",
                )

    def test_print_report_missing_headers(self) -> None:
        """
        Tests that print_report handles cases where headers might be missing from the result dict.
        """
        class TestReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {}

        report = TestReport()
        test_result = {"rows": [["Data1", "Data2"]]}

        with patch("sys.stdout", new_callable=StringIO):
            with patch("reports.base_report.tabulate") as mock_tabulate:
                report.print_report(test_result)
                mock_tabulate.assert_called_with(
                    [["Data1", "Data2"]], headers=[], tablefmt="grid", stralign="center"
                )
