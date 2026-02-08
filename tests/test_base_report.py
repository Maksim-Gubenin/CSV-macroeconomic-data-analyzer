from io import StringIO
from unittest.mock import patch

import pytest

from reports.base_report import BaseReport


class TestBaseReport:

    def test_abstract_method_raises_error(self) -> None:
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            BaseReport()  # type: ignore

    def test_concrete_class_must_implement_generate(self) -> None:
        class InvalidReport(BaseReport):  # type: ignore
            pass

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            InvalidReport()  # type: ignore

    def test_valid_concrete_class(self) -> None:
        class ValidReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {"headers": [], "rows": []}

        report = ValidReport()
        assert hasattr(report, "generate")
        assert hasattr(report, "print_report")

    def test_print_report_empty_data(self) -> None:
        class TestReport(BaseReport):
            def generate(self, data: list) -> dict:
                return {}

        report = TestReport()

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            report.print_report({})
            output = mock_stdout.getvalue()
            assert "Нет данных для отображения" in output.strip()

    def test_print_report_valid_data(self) -> None:
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
