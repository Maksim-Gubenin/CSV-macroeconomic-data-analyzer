import os
import sys
from typing import List

import pytest

from reports.base_report import BaseReport
from reports.report_factory import ReportFactory
from reports.average_gdp_report import AverageGdpReport

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class TestReportFactory:
    def setup_method(self) -> None:
        ReportFactory._reports.clear()
        ReportFactory.register_report("average-gdp", AverageGdpReport)

    def test_register_and_get_report(self) -> None:
        report = ReportFactory.get_report("average-gdp")
        assert isinstance(report, AverageGdpReport)
        assert isinstance(report, BaseReport)

    def test_get_unknown_report_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Неизвестный тип отчета: unknown"):
            ReportFactory.get_report("unknown")

    def test_get_available_reports(self) -> None:
        available = ReportFactory.get_available_reports()
        assert "average-gdp" in available
        assert len(available) == 1

    def test_register_multiple_reports(self) -> None:
        class TestReport(BaseReport):
            def generate(self, data: List[dict]) -> dict:
                return {"headers": [], "rows": []}

        ReportFactory.register_report("test-report", TestReport)
        available = ReportFactory.get_available_reports()
        assert "average-gdp" in available
        assert "test-report" in available
        assert len(available) == 2

    def test_report_instance_has_required_methods(self) -> None:
        report = ReportFactory.get_report("average-gdp")
        assert hasattr(report, "generate")
        assert hasattr(report, "print_report")
        assert callable(report.generate)
        assert callable(report.print_report)
