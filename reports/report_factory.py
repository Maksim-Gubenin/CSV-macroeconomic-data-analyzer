from typing import Dict, List, Type

from reports.base_report import BaseReport
from reports.average_gdp_report import AverageGdpReport


class ReportFactory:
    _reports: Dict[str, Type[BaseReport]] = {}
    @classmethod
    def get_report(cls, report_name: str) -> BaseReport:
        report_class = cls._reports.get(report_name)
        if not report_class:
            raise ValueError(f"Неизвестный тип отчета: {report_name}")
        return report_class()

    @classmethod
    def get_available_reports(cls) -> List[str]:
        return list(cls._reports.keys())

    @classmethod
    def register_report(cls, report_name: str, report_class: Type[BaseReport]) -> None:
        cls._reports[report_name] = report_class


ReportFactory.register_report("average-gdp", AverageGdpReport)